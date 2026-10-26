/**
 * SafeErrorHandler.ts - RFC 7807 Problem Details Error Middleware
 *
 * Implements defensive error handling:
 * 1. Zero sensitive stack trace or SQL query leaks in production.
 * 2. Emits RFC 7807 application/problem+json payload.
 * 3. Associates every incident with a unique Correlation ID.
 * 4. Differentiates operational client errors from unhandled programmer crashes.
 */

import type { Request, Response, NextFunction } from "express";
import crypto from "node:crypto";

export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance: string;
  correlationId: string;
  invalidParams?: Array<{ name: string; reason: string }>;
  stack?: string;
}

export class AppError extends Error {
  public readonly status: number;
  public readonly code: string;
  public readonly isOperational: boolean;
  public readonly invalidParams?: Array<{ name: string; reason: string }>;

  constructor(
    message: string,
    status = 500,
    code = "INTERNAL_ERROR",
    isOperational = true,
    invalidParams?: Array<{ name: string; reason: string }>
  ) {
    super(message);
    this.name = this.constructor.name;
    this.status = status;
    this.code = code;
    this.isOperational = isOperational;
    this.invalidParams = invalidParams;
    Error.captureStackTrace(this, this.constructor);
  }
}

export interface ErrorHandlerOptions {
  serviceBaseUrl?: string;
  logger?: (entry: Record<string, unknown>) => void;
  isProduction?: boolean;
}

export function createSafeErrorHandler(options: ErrorHandlerOptions = {}) {
  const isProd = options.isProduction ?? process.env.NODE_ENV === "production";
  const baseUrl = options.serviceBaseUrl || "https://errors.skillbuilder.io";
  const log = options.logger || ((entry) => console.error(JSON.stringify(entry)));

  return (err: Error | AppError, req: Request, res: Response, _next: NextFunction): void => {
    const correlationId =
      (req.headers["x-correlation-id"] as string) ||
      (req.headers["x-request-id"] as string) ||
      crypto.randomUUID();

    const isAppError = err instanceof AppError;
    const status = isAppError ? err.status : 500;
    const code = isAppError ? err.code : "INTERNAL_SERVER_ERROR";
    const isOperational = isAppError ? err.isOperational : false;

    // Sanitize detail in production for 5xx errors to prevent leaking internal topologies
    const detail = isProd && status >= 500
      ? "An unexpected internal server error occurred. Please contact support with the correlation ID."
      : err.message || "An unknown error occurred.";

    const problem: ProblemDetails = {
      type: `${baseUrl}/${code.toLowerCase().replace(/_/g, "-")}`,
      title: isAppError ? err.name : "Internal Server Error",
      status,
      detail,
      instance: req.originalUrl || req.url,
      correlationId
    };

    if (isAppError && err.invalidParams && err.invalidParams.length > 0) {
      problem.invalidParams = err.invalidParams;
    }

    if (!isProd && err.stack) {
      problem.stack = err.stack;
    }

    // Structured server log for observability
    log({
      timestamp: new Date().toISOString(),
      correlationId,
      status,
      code,
      isOperational,
      method: req.method,
      path: req.originalUrl || req.url,
      errorName: err.name,
      errorMessage: err.message,
      stack: err.stack
    });

    res.setHeader("Content-Type", "application/problem+json");
    res.setHeader("X-Correlation-ID", correlationId);
    res.status(status).json(problem);
  };
}
