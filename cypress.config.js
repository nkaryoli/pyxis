const { defineConfig } = require("cypress");
const { execFile } = require("child_process");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:5000",
    specPattern: "cypress/e2e/**/*.cy.{js,ts}",
    setupNodeEvents(on, config) {
      on("task", {
        // Runs the Python cleanup script safely from Node (used by cy.task)
        clearTestResponses(args) {
          return new Promise((resolve, reject) => {
            const allowed =
              process.env.ALLOW_DB_CLEAN === "1" ||
              process.env.FLASK_ENV === "testing" ||
              (args && args.force);
            if (!allowed) {
              // Resolve with allowed:false so the spec can decide fallback without failing the whole run
              return resolve({
                allowed: false,
                message:
                  "Not allowed: set ALLOW_DB_CLEAN=1 or FLASK_ENV=testing, or pass {force:true}",
              });
            }

            const python =
              process.platform === "win32"
                ? "venv\\Scripts\\python"
                : "venv/bin/python";
            const script = "scripts/clear_test_responses.py";

            execFile(
              python,
              [script],
              { env: { ...process.env, PYTHONIOENCODING: "utf-8", PYTHONPATH: process.cwd() } },
              (err, stdout, stderr) => {
                if (err) return reject({ error: err.message, stdout, stderr });
                return resolve({ stdout, stderr });
              },
            );
          });
        },
      });
    },
  },
});
