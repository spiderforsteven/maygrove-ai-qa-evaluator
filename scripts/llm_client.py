"""Reusable LLM client for MayGrove QA skills.

This module prefers to call the same LLM that the user is already using in
Hermes Agent. It tries, in order:

1. `hermes chat -q <prompt>` — reuses the active Hermes model/config.
2. Direct OpenAI-compatible API call based on `~/.hermes/config.yaml` and
   `~/.hermes/.env` (or `HERMES_HOME` equivalents).
3. Explicit `--model`, `--provider`, `--base-url`, `--api-key` overrides.

Supported providers (OpenAI-compatible endpoints):
  kimi-coding, kimi, moonshot, openai, openrouter, deepseek, dashscope,
  novita, glm, z.ai, minimax, arcee, opencode-zen, opencode-go.
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional


# Provider -> env var name mapping for API keys
_PROVIDER_KEY_ENV = {
    "kimi-coding": "KIMI_API_KEY",
    "kimi": "KIMI_API_KEY",
    "moonshot": "MOONSHOT_API_KEY",
    "kimi-moonshot": "KIMI_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "dashscope": "DASHSCOPE_API_KEY",
    "novita": "NOVITA_API_KEY",
    "glm": "GLM_API_KEY",
    "z.ai": "GLM_API_KEY",
    "minimax": "MINIMAX_API_KEY",
    "minimax-cn": "MINIMAX_CN_API_KEY",
    "arcee": "ARCEEAI_API_KEY",
    "arceeai": "ARCEEAI_API_KEY",
    "opencode-zen": "OPENCODE_ZEN_API_KEY",
    "opencode-go": "OPENCODE_GO_API_KEY",
}


def _hermes_executable() -> Optional[str]:
    return shutil.which("hermes")


def _run_hermes_cli(prompt: str, timeout: int = 120) -> Optional[str]:
    """Try invoking the Hermes CLI as a subprocess."""
    exe = _hermes_executable()
    if not exe:
        return None
    cmd = [exe, "chat", "-q", prompt]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        # Some versions write to stderr; try that as fallback
        if result.stderr and not result.stdout.strip():
            return result.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        print(f"[llm_client] Hermes CLI call failed: {exc}", file=sys.stderr)
    return None


def _load_env_file(path: Optional[Path]) -> dict:
    """Parse a simple KEY=VALUE env file."""
    env: dict = {}
    if not path or not path.exists():
        return env
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    except Exception as exc:
        print(f"[llm_client] Could not read env file {path}: {exc}", file=sys.stderr)
    return env


def _find_hermes_config() -> Optional[Path]:
    """Locate Hermes config.yaml using HERMES_HOME, HOME, or a known fallback."""
    candidates = []
    hermes_home = os.getenv("HERMES_HOME")
    if hermes_home:
        candidates.append(Path(hermes_home) / "config.yaml")
    candidates.append(Path.home() / ".hermes" / "config.yaml")
    # Fallback for environments where HOME is set to a nested path
    if Path.home().as_posix() != "/home/hermeswebui":
        candidates.append(Path("/home/hermeswebui/.hermes") / "config.yaml")
    for p in candidates:
        if p.exists():
            return p
    return None


def _find_hermes_env() -> Optional[Path]:
    """Locate Hermes .env file."""
    candidates = []
    hermes_home = os.getenv("HERMES_HOME")
    if hermes_home:
        candidates.append(Path(hermes_home) / ".env")
    candidates.append(Path.home() / ".hermes" / ".env")
    if Path.home().as_posix() != "/home/hermeswebui":
        candidates.append(Path("/home/hermeswebui/.hermes") / ".env")
    for p in candidates:
        if p.exists():
            return p
    return None


def _read_hermes_config() -> dict:
    """Read config.yaml and return the model section."""
    path = _find_hermes_config()
    if not path:
        return {}
    try:
        import yaml
    except ImportError:
        print(
            "[llm_client] PyYAML is not installed. Install it to read Hermes config directly.",
            file=sys.stderr,
        )
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cfg.get("model", {}) if cfg else {}
    except Exception as exc:
        print(f"[llm_client] Failed to read Hermes config: {exc}", file=sys.stderr)
    return {}


def _get_api_key(provider: str, env: dict) -> Optional[str]:
    """Look up the API key for a provider from the environment or env file."""
    provider = (provider or "").lower()
    key_name = _PROVIDER_KEY_ENV.get(provider)
    if not key_name:
        return None
    return os.getenv(key_name) or env.get(key_name)


def _default_base_url(provider: str) -> Optional[str]:
    """Return a default OpenAI-compatible base URL for common providers."""
    p = (provider or "").lower()
    if p in ("kimi-coding", "kimi"):
        return os.getenv("KIMI_BASE_URL", "https://api.kimi.com/coding")
    if p == "moonshot":
        return os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
    if p == "openai":
        return "https://api.openai.com/v1"
    if p == "openrouter":
        return "https://openrouter.ai/api/v1"
    if p == "deepseek":
        return os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    if p == "dashscope":
        return "https://dashscope.aliyuncs.com/compatible-mode/v1"
    if p == "novita":
        return os.getenv("NOVITA_BASE_URL", "https://api.novita.ai/v3/openai")
    if p in ("glm", "z.ai"):
        return os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    if p == "minimax":
        return os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    if p == "minimax-cn":
        return os.getenv("MINIMAX_CN_BASE_URL", "https://api.minimax.chat/v1")
    if p in ("arcee", "arceeai"):
        return os.getenv("ARCEE_BASE_URL", "https://app.arcee.ai")
    if p == "opencode-zen":
        return os.getenv("OPENCODE_ZEN_BASE_URL", "https://api.opencode.ai/zen")
    if p == "opencode-go":
        return os.getenv("OPENCODE_GO_BASE_URL", "https://api.opencode.ai/go")
    return None


def _call_openai_compatible(
    prompt: str,
    model: str,
    api_key: str,
    base_url: str,
    timeout: int = 120,
) -> str:
    """Make a direct OpenAI-compatible chat completion request."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")[:500]
        raise RuntimeError(f"LLM API HTTP error {exc.code}: {body}") from exc
    except KeyError as exc:
        raise RuntimeError(f"Unexpected LLM response format: missing key {exc}") from exc


def call_llm(
    prompt: str,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 120,
) -> str:
    """Call the user's current LLM.

    Priority:
      1. `hermes chat -q` (reuses the active Hermes session/model).
      2. Direct OpenAI-compatible API derived from Hermes config.
      3. Explicit arguments (model, provider, base_url, api_key).

    Raises RuntimeError if no LLM can be reached.
    """
    # 1. Try Hermes CLI first so we reuse the user's current model/settings.
    hermes_output = _run_hermes_cli(prompt, timeout=timeout)
    if hermes_output:
        return hermes_output

    # 2. Fall back to direct API call using Hermes config + env.
    hermes_env = _load_env_file(_find_hermes_env())
    cfg = _read_hermes_config()

    resolved_model = model or cfg.get("default")
    resolved_provider = provider or cfg.get("provider")
    resolved_base_url = base_url or cfg.get("base_url") or _default_base_url(resolved_provider)
    resolved_api_key = api_key or _get_api_key(resolved_provider, hermes_env)

    if resolved_model and resolved_provider and resolved_base_url and resolved_api_key:
        return _call_openai_compatible(
            prompt,
            resolved_model,
            resolved_api_key,
            resolved_base_url,
            timeout=timeout,
        )

    # 3. If we have explicit API key + base_url + model (even without provider), try anyway.
    if resolved_model and resolved_base_url and resolved_api_key:
        return _call_openai_compatible(
            prompt,
            resolved_model,
            resolved_api_key,
            resolved_base_url,
            timeout=timeout,
        )

    raise RuntimeError(
        "Could not call an LLM. Options:\n"
        "  • Make sure the `hermes` CLI is on PATH and configured.\n"
        "  • Set HERMES_HOME so this script can read your Hermes config.\n"
        "  • Or pass --model, --provider, --base-url, and --api-key.\n"
        "  • Or set the API key in ~/.hermes/.env (e.g., KIMI_API_KEY=...)."
    )


if __name__ == "__main__":
    # Simple CLI sanity test
    import argparse

    p = argparse.ArgumentParser(description="Test the LLM client")
    p.add_argument("prompt", default="Say hello in one word", nargs="?")
    args = p.parse_args()
    print(call_llm(args.prompt))
