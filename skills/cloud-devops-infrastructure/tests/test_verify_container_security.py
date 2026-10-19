import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_container_security import audit_dockerfile_content


class TestVerifyContainerSecurity(unittest.TestCase):
    def test_detects_root_user(self):
        dockerfile = """
        FROM node:20-alpine
        WORKDIR /app
        COPY . .
        CMD ["node", "server.js"]
        """
        issues = audit_dockerfile_content(dockerfile, "Dockerfile")
        self.assertTrue(any(i["rule"] == "DOCKER-ROOT-USER" for i in issues))

    def test_detects_leaked_env(self):
        dockerfile = """
        FROM node:20-alpine AS builder
        WORKDIR /app
        COPY .env ./
        USER 10001
        """
        issues = audit_dockerfile_content(dockerfile, "Dockerfile")
        self.assertTrue(any(i["rule"] == "DOCKER-LEAKED-ENV" for i in issues))

    def test_passes_hardened_dockerfile(self):
        dockerfile = """
        FROM node:20-alpine AS builder
        WORKDIR /app
        COPY package*.json ./
        RUN npm ci
        COPY . .
        RUN npm run build

        FROM gcr.io/distroless/nodejs20-debian12
        WORKDIR /app
        COPY --from=builder /app/dist ./dist
        USER 10001:10001
        CMD ["dist/main.js"]
        """
        issues = audit_dockerfile_content(dockerfile, "Dockerfile")
        self.assertEqual(len(issues), 0)


if __name__ == "__main__":
    unittest.main()
