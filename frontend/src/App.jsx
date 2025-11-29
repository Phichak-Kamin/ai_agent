import { useQuery } from "@tanstack/react-query";
import {
  fetchInventory,
  fetchMachines,
  fetchSchedule,
} from "./api/client.js";
import ScheduleTable from "./components/ScheduleTable.jsx";
import InventoryPanel from "./components/InventoryPanel.jsx";
import MachineStatus from "./components/MachineStatus.jsx";
import QueryConsole from "./components/QueryConsole.jsx";

export default function App() {
  const scheduleQuery = useQuery({
    queryKey: ["schedule"],
    queryFn: fetchSchedule,
  });

  const inventoryQuery = useQuery({
    queryKey: ["inventory"],
    queryFn: fetchInventory,
  });

  const machinesQuery = useQuery({
    queryKey: ["machines"],
    queryFn: fetchMachines,
    refetchInterval: 5000,
  });

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p>Smart Factory</p>
          <h1>LLM-driven pipeline control</h1>
          <p>
            FastAPI + LangGraph coordinate JSON-based plant data so you can ask
            questions in natural language.
          </p>
        </div>
      </header>

      <main>
        <div className="grid">
          <ScheduleTable entries={scheduleQuery.data ?? []} />
          <InventoryPanel snapshot={inventoryQuery.data} />
          <MachineStatus machineState={machinesQuery.data} />
        </div>
        <QueryConsole />
      </main>
    </div>
  );
}
