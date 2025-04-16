import os
from pathlib import Path

PS_PROFILE_PATH = Path("C:/src/ps_profile.ps1").resolve()

def ensure_line(lines, new_line):
    return lines if new_line in lines else lines + [new_line]

def bootstrap_ps_profile():
    print(f"🛠️ Bootstrapping PowerShell profile: {PS_PROFILE_PATH}")

    if not PS_PROFILE_PATH.exists():
        print("📄 Creating new PowerShell profile...")
        PS_PROFILE_PATH.write_text('Write-Host "Good morning, sir"\n\n')

    lines = PS_PROFILE_PATH.read_text().splitlines()

    updated_lines = list(lines)

    # Add PYTHONPATH
    updated_lines = ensure_line(updated_lines, '$env:PYTHONPATH = "C:\\src"')

    # Add `foz` alias
    updated_lines = ensure_line(updated_lines, 'function foz { python -m fozzie @args }')

    # Add `pe` alias (edit profile)
    updated_lines = ensure_line(updated_lines, 'Set-Alias pe Edit-Profile')
    updated_lines = ensure_line(updated_lines, 'function Edit-Profile { code "C:\\src\\ps_profile.ps1" }')

    # Add `pr` alias (reload profile)
    updated_lines = ensure_line(updated_lines, 'Set-Alias pr Reset-Profile')
    updated_lines = ensure_line(updated_lines, 'function Reset-Profile {')
    updated_lines = ensure_line(updated_lines, '    . "C:\\src\\ps_profile.ps1"')
    updated_lines = ensure_line(updated_lines, '    Write-Host "✅ PowerShell profile reloaded from C:\\src\\ps_profile.ps1" -ForegroundColor Green')
    updated_lines = ensure_line(updated_lines, '}')

    # Write the updated file
    PS_PROFILE_PATH.write_text("\n".join(updated_lines) + "\n")
    print("✅ PowerShell profile updated.")

    print("\n👉 Run this to apply the changes:")
    print("   pr")

if __name__ == "__main__":
    bootstrap_ps_profile()
