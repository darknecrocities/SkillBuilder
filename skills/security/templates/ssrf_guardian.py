#!/usr/bin/env python3
"""
ssrf_guardian.py - Server-Side Request Forgery (SSRF) Validation & Outbound Safe Fetch

Defensive controls:
1. Whitelists URL schemes (http, https only).
2. Resolves DNS and blocks private (RFC 1918), loopback, link-local, and cloud metadata IPs.
3. Mitigates DNS rebinding by connecting directly to the validated IP.
"""

import ipaddress
import socket
import sys
import urllib.parse
from typing import List, Tuple
import http.client


class SSRFSecurityViolation(Exception):
    """Raised when an outbound URL targets a prohibited or internal address space."""
    pass


PROHIBITED_METADATA_IPS = {
    "169.254.169.254",  # AWS/GCP/Azure link-local metadata
    "100.100.100.200",  # Alibaba Cloud metadata
}


def resolve_and_validate_host(hostname: str, port: int) -> List[str]:
    """
    Resolves hostname to IP addresses and asserts they belong strictly
    to public, globally-routable address spaces.
    """
    try:
        addr_info = socket.getaddrinfo(hostname, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror as err:
        raise SSRFSecurityViolation(f"DNS resolution failed for host '{hostname}': {err}")

    validated_ips: List[str] = []

    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        if ip_str in PROHIBITED_METADATA_IPS:
            raise SSRFSecurityViolation(f"SSRF Alert: Prohibited cloud metadata IP address: {ip_str}")

        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            raise SSRFSecurityViolation(f"Invalid IP address returned from DNS: {ip_str}")

        if ip_obj.is_private:
            raise SSRFSecurityViolation(f"SSRF Alert: Prohibited private IP range (RFC 1918): {ip_str}")
        if ip_obj.is_loopback:
            raise SSRFSecurityViolation(f"SSRF Alert: Prohibited loopback address: {ip_str}")
        if ip_obj.is_link_local:
            raise SSRFSecurityViolation(f"SSRF Alert: Prohibited link-local address: {ip_str}")
        if ip_obj.is_multicast:
            raise SSRFSecurityViolation(f"SSRF Alert: Prohibited multicast address: {ip_str}")
        if ip_obj.is_reserved:
            raise SSRFSecurityViolation(f"SSRF Alert: Prohibited reserved address space: {ip_str}")

        validated_ips.append(ip_str)

    if not validated_ips:
        raise SSRFSecurityViolation(f"No valid public IP addresses resolved for '{hostname}'.")

    return validated_ips


def validate_outbound_url(target_url: str) -> Tuple[str, str, int, str]:
    """
    Parses and verifies URL scheme and resolved IP.
    Returns (scheme, hostname, port, safe_ip).
    """
    parsed = urllib.parse.urlparse(target_url)
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise SSRFSecurityViolation(f"Prohibited URL scheme '{scheme}'. Only http and https are permitted.")

    hostname = parsed.hostname
    if not hostname:
        raise SSRFSecurityViolation("Missing or invalid hostname in URL.")

    port = parsed.port or (443 if scheme == "https" else 80)
    validated_ips = resolve_and_validate_host(hostname, port)

    # Pin the first validated IP address to mitigate DNS rebinding
    return scheme, hostname, port, validated_ips[0]


def safe_http_get(target_url: str, timeout_sec: float = 5.0) -> Tuple[int, bytes]:
    """
    Executes an HTTP GET request pinned to the validated IP address,
    preventing DNS rebinding (TOCTOU) attacks.
    """
    scheme, hostname, port, safe_ip = validate_outbound_url(target_url)
    parsed = urllib.parse.urlparse(target_url)
    path = parsed.path or "/"
    if parsed.query:
        path += f"?{parsed.query}"

    headers = {
        "Host": hostname,
        "User-Agent": "SkillBuilder-SSRF-Guardian/1.0",
        "Accept": "*/*",
        "Connection": "close"
    }

    if scheme == "https":
        import ssl
        ctx = ssl.create_default_context()
        conn = http.client.HTTPSConnection(safe_ip, port=port, timeout=timeout_sec, context=ctx)
    else:
        conn = http.client.HTTPConnection(safe_ip, port=port, timeout=timeout_sec)

    try:
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        body = res.read(1024 * 512)  # Cap read to 512 KB to prevent memory exhaustion
        return res.status, body
    finally:
        conn.close()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 ssrf_guardian.py <url>")
        return 1

    url = sys.argv[1]
    try:
        scheme, host, port, ip = validate_outbound_url(url)
        print(f"[PASS] Safe Outbound Target: {scheme}://{host}:{port} -> Pinned IP: {ip}")
        return 0
    except SSRFSecurityViolation as err:
        print(f"[BLOCKED] {err}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
