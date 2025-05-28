#!/usr/bin/env python3
"""Fact Checker CLI - Identify false or misleading claims in text or lint Python code."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import requests
from newspaper import Article, ArticleException
from pydantic import BaseModel, Field

# API configuration
API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY_ENV_VAR = "PPLX_API_KEY"
API_KEY_FILE = "pplx_api_key"
DEFAULT_PROMPT_FILE = "fact_checker_prompt.md"


class FactCheckResult(BaseModel):
    """Structured output format for fact check results."""
    claim: str = Field(..., description="The specific claim or statement that was evaluated")
    verdict: str = Field(..., description="Verdict on the claim's veracity (e.g., True, False, Misleading, Unverifiable)")
    explanation: str = Field(..., description="Detailed explanation of the verdict, including reasoning and evidence")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level in the verdict (0.0 to 1.0)")
    sources: list[str] = Field(default_factory=list, description="List of sources or references supporting the explanation")


class FactChecker:
    """Fact Checker using Perplexity API."""
    DEFAULT_MODEL = "sonar-medium-online"

    def __init__(self, api_key: Optional[str] = None, prompt_file: Optional[str] = None):
        """Initialize with API key and optional custom prompt file."""
        self.api_key = api_key or self._load_api_key()
        self.system_prompt = self._load_system_prompt(prompt_file)

    def _load_api_key(self) -> str:
        """Load API key from environment variable or file."""
        if api_key := os.getenv(API_KEY_ENV_VAR):
            return api_key
        try:
            with open(API_KEY_FILE, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise ValueError(
                f"API key not found in environment variable {API_KEY_ENV_VAR} or file {API_KEY_FILE}. "
                f"Please set the API key using the -k/--api-key option, "
                f"export it as an environment variable, or store it in a file named {API_KEY_FILE}."
            )

    def _load_system_prompt(self, prompt_file: Optional[str] = None) -> str:
        """Load system prompt from file or use default."""
        file_to_load = prompt_file or DEFAULT_PROMPT_FILE
        try:
            with open(file_to_load, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            if prompt_file:
                raise FileNotFoundError(f"Prompt file {prompt_file} not found.")
            return (
                "You are an expert fact checker. Your task is to evaluate the accuracy of claims or statements provided. "
                "For each claim, provide a clear verdict (e.g., True, False, Misleading, Unverifiable), a detailed explanation, "
                "a confidence level (0.0 to 1.0), and a list of credible sources if available. Respond in a structured JSON format "
                "if requested, adhering to the specified schema."
            )

    def check(self, text: str, model: str = DEFAULT_MODEL, structured_output: bool = False) -> dict:
        """Fact check the provided text using Perplexity API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Fact check the following text:\n\n{text}"},
        ]
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if structured_output and "sonar" in model:
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}") from e


def read_file(file_path: str) -> str:
    """Read content from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {str(e)}") from e


def extract_article(url: str) -> str:
    """Extract text content from a URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except ArticleException as e:
        raise RuntimeError(f"Failed to extract article from {url}: {str(e)}") from e


def lint_python_files(directory: str = ".") -> dict:
    """
    Recursively find all Python files in the given directory and run pylint on them.
    
    Args:
        directory: The root directory to start the search from (default: current directory)
    
    Returns:
        A dictionary with linting results or errors for each file
    """
    results = {}
    python_files = list(Path(directory).rglob("*.py"))
    
    if not python_files:
        return {"error": "No Python files found in the directory or subdirectories."}
    
    for file_path in python_files:
        try:
            # Run pylint on the file
            cmd = ["pylint", str(file_path)]
            process = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            results[str(file_path)] = {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "returncode": process.returncode
            }
        except FileNotFoundError:
            return {"error": "pylint not found. Please install it using 'pip install pylint'."}
        except Exception as e:
            results[str(file_path)] = {"error": f"Failed to lint file: {str(e)}"}
    
    return results


def display_lint_results(results: dict, format_json: bool = False):
    """
    Display linting results for each file.
    
    Args:
        results: Dictionary with linting results for each file
        format_json: Whether to display results as JSON
    """
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    
    if format_json:
        print(json.dumps(results, indent=2))
        return
    
    print("\n📋 LINTING RESULTS:")
    for file_path, result in results.items():
        print(f"\nFile: {file_path}")
        if "error" in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Return Code: {result['returncode']}")
            if result['stdout']:
                print(f"  Output:\n{result['stdout']}")
            if result['stderr']:
                print(f"  Errors/Warnings:\n{result['stderr']}")


def display_result(response: dict, format_json: bool = False):
    """Display the fact check result."""
    try:
        content = response["choices"][0]["message"]["content"]
        if format_json:
            print(content)
            return
        if isinstance(content, dict) or (isinstance(content, str) and content.strip().startswith("{")):
            if isinstance(content, str):
                content = json.loads(content)
            result = FactCheckResult(**content)
            print(f"\n🔍 FACT CHECK RESULT:")
            print(f"Claim: {result.claim}")
            print(f"Verdict: {result.verdict}")
            print(f"Explanation: {result.explanation}")
            print(f"Confidence: {result.confidence:.2%}")
            if result.sources:
                print("Sources:")
                for source in result.sources:
                    print(f"  - {source}")
        else:
            print(f"\n🔍 FACT CHECK RESULT:")
            print(content)
    except (KeyError, json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing response: {str(e)}", file=sys.stderr)
        print(f"Raw response: {json.dumps(response, indent=2)}", file=sys.stderr)


def main() -> int:
    """Main entry point for the fact checker CLI."""
    parser = argparse.ArgumentParser(
        description="Fact Checker CLI - Identify false or misleading claims or lint Python code"
    )
    
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument("-t", "--text", type=str, help="Text to fact check")
    input_group.add_argument("-f", "--file", type=str, help="Path to file containing text to fact check")
    input_group.add_argument("-u", "--url", type=str, help="URL of the article to fact check")
    
    parser.add_argument("-l", "--lint", action="store_true", help="Lint all Python files in the current directory and subdirectories")
    parser.add_argument("-m", "--model", type=str, default=FactChecker.DEFAULT_MODEL, help=f"Perplexity model to use (default: {FactChecker.DEFAULT_MODEL})")
    parser.add_argument("-k", "--api-key", type=str, help="Perplexity API key")
    parser.add_argument("-p", "--prompt-file", type=str, help=f"Path to file containing the system prompt")
    parser.add_argument("-j", "--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--structured-output", action="store_true", help="Enable structured output format")
    
    args = parser.parse_args()
    
    if args.lint:
        print("Linting all Python files in current directory and subdirectories...", file=sys.stderr)
        lint_results = lint_python_files()
        display_lint_results(lint_results, format_json=args.json)
        return 0
    
    if not any([args.text, args.file, args.url]):
        parser.error("One of --text, --file, or --url must be provided for fact checking.")
    
    try:
        fact_checker = FactChecker(api_key=args.api_key, prompt_file=args.prompt_file)
        if args.text:
            text = args.text
        elif args.file:
            text = read_file(args.file)
        else:  # args.url
            text = extract_article(args.url)
        
        print(f"Fact checking content... (model: {args.model})", file=sys.stderr)
        response = fact_checker.check(text, model=args.model, structured_output=args.structured_output)
        display_result(response, format_json=args.json)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
