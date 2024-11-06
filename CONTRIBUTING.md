# Contribution Guide

Thank you for considering contributing to KitPass! We appreciate any improvements, whether it’s a new feature, bug fix, or documentation update. This guide will help you get started and ensure that all contributions are consistent and maintainable.

## Getting Started

1. **Fork the repository**: Start by forking the KitPass repository to your own GitHub account.
2. **Clone your fork**: Clone your fork locally to work on it:
   ```bash
   git clone https://github.com/<your-username>/KitPass.git
   ```
3. **Create a new branch**: Create a new branch for your feature or fix. Be sure to use a descriptive name:
   ```bash
   git checkout -b <feature-or-fix-name>
   ```

4. **Make your changes**: Work on your feature or fix. Ensure your code follows the existing style and best practices.

5. **Run tests**: If you’re modifying the code, make sure to run any tests to verify your changes.

6. **Commit your changes**: Once your changes are ready, commit them using the conventions below.

7. **Push your changes**: Push your changes back to your fork:
   ```bash
   git push origin <feature-or-fix-name>
   ```

8. **Create a pull request**: Open a pull request (PR) to the `main` branch of the KitPass repository.

## Commit Conventions

To keep the Git history clean and readable, please follow these commit message conventions. This will help maintain a consistent history for the project.

### 1. **Structure**
Each commit message should have the following structure:
```
<type>: <short description>

<optional detailed description>
```

### 2. **Types**
Use the following commit types to categorize your changes:

- **feat**: A new feature or enhancement to an existing feature.
- **fix**: A bug fix.
- **docs**: Changes to documentation only.
- **style**: Code formatting changes (e.g., whitespace, indentation) that do not affect functionality.
- **refactor**: Code changes that neither fix a bug nor add a feature, typically to improve code quality or readability.
- **perf**: Performance improvements.
- **test**: Adding or modifying tests.
- **chore**: Routine changes, such as updating dependencies or other non-code tasks.

### 3. **Examples**

- `feat: add export data feature`
- `fix: resolve crash on Android 11`
- `docs: update README with contribution guidelines`
- `style: fix indentation in export functions`
- `refactor: simplify import/export logic`
- `perf: optimize image compression for faster load times`
- `test: add unit tests for export function`
- `chore: update dependencies`

## Submitting Issues

If you find a bug or have an idea for a new feature, please [open an issue](https://github.com/<your-username>/KitPass/issues). When submitting an issue, provide as much information as possible to help us understand and replicate the problem:

- **Describe the problem** clearly.
- **Provide steps to reproduce** the issue.
- **Include relevant logs** or error messages if applicable.

## Code of Conduct

By contributing to this project, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md). We expect everyone to engage respectfully and thoughtfully in discussions.