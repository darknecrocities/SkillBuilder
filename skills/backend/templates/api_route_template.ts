import { Request, Response, NextFunction } from "express";
import { z } from "zod";

export const CreateProjectSchema = z.object({
  name: z.string().min(3).max(50).trim(),
  description: z.string().max(250).optional(),
});

export type CreateProjectInput = z.infer<typeof CreateProjectSchema>;

export async function createProjectHandler(req: Request, res: Response, next: NextFunction) {
  try {
    // 1. Boundary Schema Validation
    const parsed = CreateProjectSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        type: "https://api.example.com/errors/validation-error",
        title: "Validation Error",
        status: 400,
        detail: "The request body failed schema validation.",
        invalid_params: parsed.error.issues.map((i) => ({
          field: i.path.join("."),
          message: i.message,
        })),
      });
    }

    // 2. Delegate to Domain Service
    const project = { id: "proj_123", ...parsed.data, createdAt: new Date().toISOString() };

    // 3. Return RFC-compliant response
    return res.status(201).json({ data: project });
  } catch (error) {
    return next(error);
  }
}
