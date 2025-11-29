import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { postOwnerQuery } from "../api/client";

export default function QueryConsole() {
  const [message, setMessage] = useState("");
  const { mutateAsync, data, isPending } = useMutation({
    mutationFn: postOwnerQuery,
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!message.trim()) {
      return;
    }
    await mutateAsync({ message });
    setMessage("");
  };

  return (
    <section className="panel">
      <header className="panel__header">
        <div>
          <h2>Owner Console</h2>
          <p>Ask anything about schedule, stock, or machines.</p>
        </div>
      </header>
      <div className="panel__body console">
        <form onSubmit={handleSubmit}>
          <label htmlFor="console-input">Prompt</label>
          <textarea
            id="console-input"
            rows={4}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="e.g. Add 100 units of widget_a before noon"
          />
          <button type="submit" disabled={isPending}>
            {isPending ? "Sending..." : "Send"}
          </button>
        </form>
        <div className="console__output">
          <h3>Latest Response</h3>
          {data ? (
            <pre>{JSON.stringify(data, null, 2)}</pre>
          ) : (
            <p>No messages yet.</p>
          )}
        </div>
      </div>
    </section>
  );
}
