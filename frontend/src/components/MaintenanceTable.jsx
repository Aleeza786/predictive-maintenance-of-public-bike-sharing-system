export default function MaintenanceTable({ data }) {
  return (
    <table className="min-w-full text-left border border-gray-200 rounded-lg">
      <thead className="bg-accent text-white">
        <tr>
          <th className="px-4 py-2">Record ID</th>
          <th className="px-4 py-2">Bike ID</th>
          <th className="px-4 py-2">Date</th>
          <th className="px-4 py-2">Component Failed</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} className="border-b hover:bg-gray-100">
            <td className="px-4 py-2">{row.record_id}</td>
            <td className="px-4 py-2">{row.bike_id}</td>
            <td className="px-4 py-2">{row.maintenance_date}</td>
            <td className="px-4 py-2 text-danger font-semibold">{row.component_failed}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
