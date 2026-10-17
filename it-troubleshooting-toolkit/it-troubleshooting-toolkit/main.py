
import socket
import urllib.request
import urllib.error
import platform
import subprocess


def check_dns(hostname="example.com"):
    """Check whether a domain name can be resolved."""
    print("\n[1] DNS Resolution")

    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"SUCCESS: {hostname} resolved to {ip_address}")
        return True

    except socket.gaierror:
        print("FAILED: Could not resolve the domain name.")
        print("Tip: Check your DNS settings or try another network.")
        return False


def check_internet():
    """Check whether an HTTPS connection can be established."""
    print("\n[2] Internet Connectivity")

    url = "https://example.com"

    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "IT-Troubleshooting-Toolkit/1.0"}
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            print(f"SUCCESS: HTTPS connection returned status {response.status}")
            return True

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"FAILED: Could not complete the HTTPS check ({error}).")
        print("Tip: Check your Wi-Fi, network connection, or firewall.")
        return False


def check_ping(host="1.1.1.1"):
    """Check whether a host responds to a ping request."""
    print("\n[3] Ping Test")

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "3000", host]
    else:
        command = ["ping", "-c", "1", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print(f"SUCCESS: {host} responded to ping.")
            return True

        print(f"FAILED: No successful ping response from {host}.")
        print("Tip: ICMP traffic may be blocked by a firewall or network.")
        return False

    except (OSError, subprocess.TimeoutExpired):
        print("FAILED: Could not complete the ping test.")
        print("Tip: Check that the ping command is available.")
        return False


def main():
    print("=" * 42)
    print("       IT TROUBLESHOOTING TOOLKIT")
    print("=" * 42)

    results = [
        check_dns(),
        check_internet(),
        check_ping()
    ]

    passed = sum(results)

    print("\n" + "=" * 42)
    print(f"RESULTS: {passed} of {len(results)} checks passed.")
    print("=" * 42)

    if passed == len(results):
        print("All checks passed.")
    else:
        print("One or more checks failed. Review the tips above.")


if __name__ == "__main__":
    main()