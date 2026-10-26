/**
 * TokenVault.ts - Cryptographic Token Generation, Constant-Time Compare & Rotation
 *
 * Implements defensive authentication hygiene:
 * 1. Constant-time string equality mitigating timing side-channel attacks.
 * 2. High-entropy cryptographically secure random token generation.
 * 3. Refresh token family rotation with automated reuse detection and family revocation.
 */

import crypto from "node:crypto";

export interface TokenRecord {
  tokenHash: string;
  familyId: string;
  userId: string;
  isRevoked: boolean;
  createdAt: number;
  expiresAt: number;
}

export class TokenVault {
  private readonly tokenFamilies = new Map<string, Set<string>>(); // familyId -> Set<tokenHash>
  private readonly tokens = new Map<string, TokenRecord>();          // tokenHash -> TokenRecord

  /**
   * Generates a high-entropy URL-safe cryptographic token string.
   */
  public static generateSecureToken(byteLength = 32): string {
    return crypto.randomBytes(byteLength).toString("base64url");
  }

  /**
   * Performs constant-time string comparison to prevent timing side-channel attacks.
   */
  public static timingSafeCompare(a: string, b: string): boolean {
    const bufA = Buffer.from(a, "utf8");
    const bufB = Buffer.from(b, "utf8");

    if (bufA.length !== bufB.length) {
      // Execute dummy comparison to maintain constant time execution profile
      crypto.timingSafeEqual(bufA, bufA);
      return false;
    }
    return crypto.timingSafeEqual(bufA, bufB);
  }

  /**
   * Computes SHA-256 hash of a raw token for safe persistence.
   */
  public static hashToken(rawToken: string): string {
    return crypto.createHash("sha256").update(rawToken).digest("hex");
  }

  /**
   * Issues a brand new refresh token family for an authenticated user session.
   */
  public issueNewFamily(userId: string, ttlMs = 7 * 24 * 60 * 60 * 1000): { rawToken: string; familyId: string } {
    const rawToken = TokenVault.generateSecureToken(32);
    const tokenHash = TokenVault.hashToken(rawToken);
    const familyId = crypto.randomUUID();
    const now = Date.now();

    const record: TokenRecord = {
      tokenHash,
      familyId,
      userId,
      isRevoked: false,
      createdAt: now,
      expiresAt: now + ttlMs
    };

    this.tokens.set(tokenHash, record);
    this.tokenFamilies.set(familyId, new Set([tokenHash]));

    return { rawToken, familyId };
  }

  /**
   * Rotates a refresh token.
   * If a used/revoked token is presented, detects compromise and revokes the entire family!
   */
  public rotateToken(
    rawToken: string,
    ttlMs = 7 * 24 * 60 * 60 * 1000
  ): { success: boolean; newRawToken?: string; userId?: string; compromiseDetected?: boolean } {
    const incomingHash = TokenVault.hashToken(rawToken);
    const existing = this.tokens.get(incomingHash);

    if (!existing) {
      return { success: false, compromiseDetected: false };
    }

    // Check if token has expired
    if (Date.now() > existing.expiresAt) {
      this.tokens.delete(incomingHash);
      return { success: false, compromiseDetected: false };
    }

    // TOKEN REUSE DETECTED: This token was already rotated/revoked!
    if (existing.isRevoked) {
      this.revokeFamily(existing.familyId);
      return { success: false, compromiseDetected: true };
    }

    // Legitimate rotation: Revoke current token and issue new token in the same family
    existing.isRevoked = true;

    const newRawToken = TokenVault.generateSecureToken(32);
    const newHash = TokenVault.hashToken(newRawToken);
    const now = Date.now();

    const newRecord: TokenRecord = {
      tokenHash: newHash,
      familyId: existing.familyId,
      userId: existing.userId,
      isRevoked: false,
      createdAt: now,
      expiresAt: now + ttlMs
    };

    this.tokens.set(newHash, newRecord);
    const familySet = this.tokenFamilies.get(existing.familyId);
    if (familySet) {
      familySet.add(newHash);
    }

    return { success: true, newRawToken, userId: existing.userId };
  }

  /**
   * Revokes every token belonging to a compromised or logged-out token family.
   */
  public revokeFamily(familyId: string): void {
    const familySet = this.tokenFamilies.get(familyId);
    if (!familySet) return;

    for (const hash of familySet) {
      const record = this.tokens.get(hash);
      if (record) {
        record.isRevoked = true;
      }
    }
    this.tokenFamilies.delete(familyId);
  }
}
