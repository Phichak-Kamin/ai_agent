export default function InventoryPanel({ snapshot }) {
  const { materials_available = {}, materials_usage = {} } = snapshot ?? {};
  return (
    <section className="panel">
      <header className="panel__header">
        <div>
          <h2>Inventory</h2>
          <p>Local JSON snapshot of inventory and per-product consumption.</p>
        </div>
      </header>
      <div className="panel__body inventory">
        <div>
          <h3>Available</h3>
          <ul>
            {Object.entries(materials_available).map(([material, qty]) => (
              <li key={material}>
                <span>{material}</span>
                <span>{qty}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Usage per Product</h3>
          <ul>
            {Object.entries(materials_usage).map(([product, usage]) => (
              <li key={product}>
                <span>{product}</span>
                <span>
                  {Object.entries(usage)
                    .map(([material, qty]) => `${material}:${qty}`)
                    .join(", ")}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
