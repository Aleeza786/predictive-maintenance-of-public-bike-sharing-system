export default function RiskTable({ data }) {
  return (
    <table className="min-w-full text-left border border-gray-200 rounded-lg">
      <thead className="bg-primary text-white">
        <tr>
          <th className="px-4 py-2">Bike ID</th>
          <th className="px-4 py-2">Risk Score</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} className="border-b hover:bg-gray-100">
            <td className="px-4 py-2">{row.bike_id}</td>
            <td className="px-4 py-2 text-danger font-semibold">
              {(row.risk_score * 100).toFixed(2)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
