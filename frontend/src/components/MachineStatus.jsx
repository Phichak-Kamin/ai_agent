export default function MachineStatus({ machineState }) {
  const { states = {}, durations = {} } = machineState ?? {};
  return (
    <section className="panel">
      <header className="panel__header">
        <div>
          <h2>Machine Deck</h2>
          <p>Reports toggle state (1=idle, 0=busy) and runtime in seconds.</p>
        </div>
      </header>
      <div className="panel__body">
        <table className="table">
          <thead>
            <tr>
              <th>Machine</th>
              <th>Status</th>
              <th>Runtime (s)</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(states).map(([machine, status]) => (
              <tr key={machine}>
                <td>{machine}</td>
                <td className={status === 0 ? "status--busy" : "status--idle"}>
                  {status === 0 ? "In Use" : "Ready"}
                </td>
                <td>{(durations[machine] ?? 0).toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
