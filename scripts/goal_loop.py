#!/usr/bin/env python3
"""
goal_loop.py — Run a goal through multiple agent iterations with validation.
Uses Hermes Agent's delegate_task tool via the hermes_tools Python API.

Usage:
   python3 goal_loop.py "Build a Pomodoro timer with tests" --max-iterations 5
"""

import sys
import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Run a goal through agent loops")
    parser.add_argument("goal", help="The goal to achieve")
    parser.add_argument("--max-iterations", type=int, default=5, help="Maximum agent iterations")
    args = parser.parse_args()

    goal = args.goal
    max_iterations = args.max_iterations

    print(f"🎯 Goal: {goal}")
    print(f"🔁 Max iterations: {max_iterations}")
    print()

    # The actual loop logic needs to run INSIDE a Hermes session
    # (where delegate_task tool is available).
    # This script is a WRAPPER that tells Hermes to run the loop.
    #
    # Proper usage:
    #   In a Hermes session, call:
    #     delegate_task(
    #       goal='Run goal_loop for: "Build a Pomodoro timer"',
    #       context='...',
    #       role='orchestrator'
    #     )
    #
    # For now, this script outputs the prompt for the orchestrator.

    orchestrator_prompt = f"""
You are running a Goal Mode loop for Tom's AI agent setup.

GOAL: {goal}

INSTRUCTIONS:
1. Spawn a leaf subagent with `delegate_task` to work on the goal.
2. The leaf should write code/tests to `/tmp/goal_loop_output/`.
3. After the leaf finishes, VALIDATE the output:
   - Do tests pass? (run `python3 -m pytest /tmp/goal_loop_output/`)
   - Is the code complete?
4. If validation fails, spawn ANOTHER leaf with error context.
5. Repeat up to {max_iterations} iterations.
6. When succeeded, save the result and report back.

Use `delegate_task` (not shell commands) for each iteration.
Each leaf gets the goal + error context from previous attempts.
""".strip()

    print("📋 Orchestrator prompt (paste into Hermes):")
    print()
    print(orchestrator_prompt)
    print()
    print("💡 To run this:")
    print("   1. Open Hermes")
    print("   2. Call delegate_task with the prompt above")
    print("   3. The orchestrator will handle the loop automatically")

if __name__ == "__main__":
    main()
