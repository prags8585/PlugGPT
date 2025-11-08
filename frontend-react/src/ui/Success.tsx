import React from "react";
import { useSearchParams } from "react-router-dom";

export default function Success() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session_id");

  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center text-slate-100">
      <h1 className="text-4xl font-bold mb-4 text-green-400">🎉 Payment Successful!</h1>
      <p className="text-lg mb-2">Thank you for your purchase.</p>
      {sessionId && (
        <p className="text-sm text-slate-400">
          Your Stripe session ID: <span className="text-slate-300">{sessionId}</span>
        </p>
      )}
      <a href="/" className="mt-6 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 rounded-xl font-semibold">
        Back to Home
      </a>
    </div>
  );
}
