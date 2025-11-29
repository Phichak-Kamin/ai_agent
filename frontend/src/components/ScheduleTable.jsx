const columns = ["Order", "Product", "Qty", "Process Time (s)", "Deadline"];

export default function ScheduleTable({ entries = [] }) {
  return (
    <section className="panel">
      <header className="panel__header">
        <div>
          <h2>Production Schedule</h2>
          <p>Orders currently orchestrated by the LangGraph agent.</p>
        </div>
      </header>
      <div className="panel__body">
        <table className="table">
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {entries.map((entry) => (
              <tr key={entry.order_id}>
                <td>{entry.order_id}</td>
                <td>{entry.product}</td>
                <td>{entry.quantity}</td>
                <td>{entry.process_time_sec}</td>
                <td>{new Date(entry.deadline).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
