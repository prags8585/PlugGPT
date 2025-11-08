// import React, { useState } from "react";

// const API = "http://localhost:8000/api";

// function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement>) {
//   return (
//     <button
//       className="px-4 py-2 rounded-xl bg-indigo-500 hover:bg-indigo-600 font-semibold"
//       {...props}
//     />
//   );
// }

// export default function App() {
//   const [prompt, setPrompt] = useState("Add Firebase login and Stripe subscriptions and deploy to GCP");
//   const [output, setOutput] = useState("");
//   const [status, setStatus] = useState("");

//   const plan = async () => {
//     setStatus("Planning...");
//     const res = await fetch(`${API}/plan`, {
//       method: "POST",
//       headers: {"Content-Type":"application/json"},
//       body: JSON.stringify({ prompt })
//     });
//     const data = await res.json();
//     (window as any).__PLAN__ = data;
//     setOutput(JSON.stringify(data, null, 2));
//     setStatus("Plan ready.");
//   };

//   const generate = async () => {
//     setStatus("Generating...");
//     const plan = (window as any).__PLAN__ || { integrations:[{name:"firebase_auth"},{name:"stripe_payments"}], deployment:{platform:"gcp_cloud_run","iac":"terraform"} };
//     const res = await fetch(`${API}/generate`, {
//       method: "POST",
//       headers: {"Content-Type":"application/json"},
//       body: JSON.stringify({ plan, project_name: "demo_app" })
//     });
//     const data = await res.json();
//     setOutput(JSON.stringify(data, null, 2));
//     setStatus("Project generated at backend/workspace/demo_app");
//   };

//   const secrets = async () => {
//     setStatus("Appending secrets (demo only)...");
//     const values = {
//       STRIPE_SECRET_KEY: "sk_test_replace",
//       STRIPE_WEBHOOK_SECRET: "whsec_replace",
//       FIREBASE_PROJECT_ID: "your_project",
//       FIREBASE_CLIENT_EMAIL: "svc@your_project.iam.gserviceaccount.com",
//       FIREBASE_PRIVATE_KEY: "-----BEGIN PRIVATE KEY-----\\nREPLACE\\n-----END PRIVATE KEY-----\\n"
//     };
//     const res = await fetch(`${API}/secrets`, {
//       method: "POST",
//       headers: {"Content-Type":"application/json"},
//       body: JSON.stringify({ project_name: "demo_app", values })
//     });
//     const data = await res.json();
//     setOutput(JSON.stringify(data, null, 2));
//     setStatus("Secrets appended to workspace/demo_app/.env (replace later).");
//   };

//   const deployLocal = async () => {
//     setStatus("Deploying (local)...");
//     const res = await fetch(`${API}/deploy?project_name=demo_app&target=local`, { method: "POST" });
//     const data = await res.json();
//     setOutput(JSON.stringify(data, null, 2));
//     setStatus("Local deploy hint ready. Now run the generated app (uvicorn).");
//   };

//   const deployCloudRun = async () => {
//     setStatus("Deploying to Cloud Run...");
//     const res = await fetch(`${API}/deploy?project_name=demo_app&target=cloud_run`, { method: "POST" });
//     const data = await res.json();
//     setOutput(JSON.stringify(data, null, 2));
//     setStatus("Cloud Run task finished (check output for URL or error).");
//   };

//   return (
//     <div className="max-w-5xl mx-auto p-6 space-y-4">
//       <h1 className="text-3xl font-bold">PlugGPT</h1>
//       <p className="text-slate-300">Describe integrations in plain English, generate a runnable app, and deploy.</p>

//       <textarea
//         value={prompt}
//         onChange={(e) => setPrompt(e.target.value)}
//         rows={4}
//         className="w-full p-3 rounded-xl bg-slate-900 border border-slate-700"
//       />

//       <div className="flex flex-wrap gap-2">
//         <Button onClick={plan}>Plan</Button>
//         <Button onClick={generate}>Generate</Button>
//         <Button onClick={secrets}>Add Secrets</Button>
//         <Button onClick={deployLocal}>Deploy (Local)</Button>
//         <Button onClick={deployCloudRun}>Deploy (Cloud Run)</Button>
//       </div>

//       <div className="text-sm text-slate-400">{status}</div>
//       <pre className="bg-slate-900 p-4 rounded-xl overflow-auto min-h-[200px]">{output}</pre>
//     </div>
//   );
// }

// 2nd latest is from 107 to 211
// import React, { useState } from "react";

// const API = "http://localhost:8000/api";

// export default function App() {
//   const [prompt, setPrompt] = useState(
//     "Add Firebase login and Stripe subscriptions and deploy to GCP"
//   );
//   const [output, setOutput] = useState("");
//   const [status, setStatus] = useState("");

//   async function call(endpoint: string, body: any = {}) {
//     setStatus(`Running ${endpoint}…`);
//     try {
//       const res = await fetch(`${API}/${endpoint}`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(body),
//       });
//       const json = await res.json();
//       setOutput(JSON.stringify(json, null, 2));
//       setStatus(`${endpoint} complete`);
//     } catch (e: any) {
//       setOutput(`{"error": "${e?.message || "Request failed"}"}`);
//       setStatus("error");
//     }
//   }

//   return (
//     <>
//       <header className="header">
//         <h1 className="title">PlugGPT</h1>
//         <p className="subtitle">
//           Describe integrations in plain English, generate a runnable app, and deploy.
//         </p>
//       </header>

//       <main className="shell">
//         {/* Left: Composer */}
//         <section className="card">
//           <textarea
//             className="textarea"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             placeholder="Describe your integration or target stack…"
//           />

//           <div className="row">
//             <button
//               className="btn"
//               onClick={() => call("plan", { prompt })}
//               title="Analyze your request and produce a plan"
//             >
//               Plan
//             </button>

//             <button
//               className="btn"
//               onClick={() =>
//                 call("generate", {
//                   project_name: "demo_app",
//                   plan: {
//                     integrations: [
//                       { name: "firebase_auth" },
//                       { name: "stripe_payments" },
//                     ],
//                     deployment: { platform: "gcp_cloud_run", iac: "terraform" },
//                   },
//                 })
//               }
//             >
//               Generate
//             </button>

//             <button
//               className="btn secondary"
//               onClick={() => call("secrets", { project_name: "demo_app", values: {} })}
//               title="Writes .env placeholders for your generated app"
//             >
//               Add Secrets
//             </button>

//             <button
//               className="btn secondary"
//               onClick={() => call("deploy", { project_name: "demo_app" })}
//               title="Local docker build / or Cloud Run if configured"
//             >
//               Deploy (Local)
//             </button>
//           </div>

//           <div className="status">{status || "Ready."}</div>
//         </section>

//         {/* Right: Output */}
//         <section className="card">
//           <div className="status">Response</div>
//           <div className="output">
//             <pre>{output || "— waiting for output —"}</pre>
//           </div>
//         </section>
//       </main>
//     </>
//   );
// }

import React, { useState } from "react";

const API = "http://localhost:8000/api";

type Plan = {
  prompt: string;
  integrations: Array<{ name: string }>;
  deployment: { platform: string; iac: string };
};

export default function App() {
  const [prompt, setPrompt] = useState(
    "Add Firebase login and Stripe subscriptions and deploy to GCP"
  );
  const [output, setOutput] = useState("");
  const [status, setStatus] = useState("");
  const [lastPlan, setLastPlan] = useState<Plan | null>(null);
  const [projectName, setProjectName] = useState<string | null>(null);

  async function call(endpoint: string, body: any = {}) {
    setStatus(`Running ${endpoint}…`);
    const res = await fetch(`${API}/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const json = await res.json();
    setOutput(JSON.stringify(json, null, 2));
    setStatus(`${endpoint} complete`);
    return json;
  }

  async function onPlan() {
    setStatus("Planning…");
    const json = await call("plan", { prompt });
    // Expect shape: { prompt, integrations:[{name}], deployment:{...} }
    setLastPlan(json);
  }

  async function onGenerate() {
    setStatus("Generating…");

    // Use the plan from /plan; if missing, fall back to a sane default
    const plan: Plan =
      lastPlan || {
        prompt,
        integrations: [{ name: "firebase_auth" }, { name: "stripe_payments" }],
        deployment: { platform: "gcp_cloud_run", iac: "terraform" },
      };

    // IMPORTANT: do NOT pass project_name; backend will derive a unique one
    const json = await call("generate", { prompt, plan });

    // Expect shape: { ok:true, result:{ project_name, project_root } }
    const name = json?.result?.project_name;
    if (name) setProjectName(name);
    setStatus(
      name
        ? `generate complete → ${name}`
        : "generate complete (check response)"
    );
  }

  async function onSecrets() {
    setStatus("Appending secrets…");

    // if we have a known project, pass it; otherwise omit and backend will use newest
    const values = {
      STRIPE_SECRET_KEY: "sk_test_replace",
      STRIPE_WEBHOOK_SECRET: "whsec_replace",
      FIREBASE_PROJECT_ID: "your_project",
      FIREBASE_CLIENT_EMAIL:
        "svc@your_project.iam.gserviceaccount.com",
      FIREBASE_PRIVATE_KEY:
        "-----BEGIN PRIVATE KEY-----\\nREPLACE\\n-----END PRIVATE KEY-----\\n",
    };

    const body = projectName ? { project_name: projectName, values } : { values };
    const json = await call("secrets", body);

    setStatus(
      `secrets complete → ${
        projectName || json?.result?.project_root?.split("/").pop() || "latest project"
      }`
    );
  }

  async function onDeployLocal() {
    setStatus("Deploying (local)…");
    const body = projectName ? { project_name: projectName, mode: "local" } : { mode: "local" };
    await call("deploy", body);
  }

  return (
    <>
      <header className="header">
        <h1 className="title">PlugGPT</h1>
        <p className="subtitle">
          Describe integrations in plain English, generate a runnable app, and deploy.
        </p>
      </header>

      <main className="shell">
        {/* Left: Composer */}
        <section className="card">
          <textarea
            className="textarea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your integration or target stack…"
          />

          <div className="row">
            <button className="btn" onClick={onPlan}>Plan</button>

            <button className="btn" onClick={onGenerate}>
              Generate
            </button>

            <button
              className="btn secondary"
              onClick={onSecrets}
              title="Writes .env placeholders for your generated app"
            >
              Add Secrets
            </button>

            <button
              className="btn secondary"
              onClick={onDeployLocal}
              title="Local docker build / or Cloud Run if configured"
            >
              Deploy (Local)
            </button>
          </div>

          <div className="status">
            {status || "Ready."}
            {projectName ? ` • current project: ${projectName}` : ""}
          </div>
        </section>

        {/* Right: Output */}
        <section className="card">
          <div className="status">Response</div>
          <div className="output">
            <pre>{output || "— waiting for output —"}</pre>
          </div>
        </section>
      </main>
    </>
  );
}

