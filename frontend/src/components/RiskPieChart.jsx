import React from "react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from "recharts";

const COLORS = [
  "#4C51BF", "#63B3ED", "#00C49F", "#F6AD55", "#E53E3E",
  "#9F7AEA", "#F6E05E", "#4FD1C5", "#F687B3", "#7DD3FC"
];

function groupTopN(data = [], topN = 8) {
  if (!data || data.length === 0) return [];
  const sorted = [...data].sort((a, b) => (b.risk_score || 0) - (a.risk_score || 0));
  const top = sorted.slice(0, topN);
  const rest = sorted.slice(topN);
  if (rest.length === 0) return top.map((d) => ({ ...d, name: `B${d.bike_id}` }));
  const otherValue = rest.reduce((s, r) => s + (r.risk_score || 0), 0);
  const other = { bike_id: "Other", risk_score: parseFloat(otherValue.toFixed(3)), name: "Other" };
  return [
    ...top.map((d) => ({ ...d, name: `B${d.bike_id}` })),
    other
  ];
}

export default function RiskPieChart({ data }) {
  const chartData = groupTopN(data, 8);

  // compute percent value for slices (0-100)
  const total = chartData.reduce((s, r) => s + (r.risk_score || 0), 0) || 1;
  const dataWithPct = chartData.map(d => ({ ...d, value: +( ((d.risk_score||0) / total) * 100 ).toFixed(2) }));

  return (
    // Add top padding so pie is not cut off; increase height to give room for legend
    <div style={{ width: "100%", height: 420, paddingTop: 18 }}>
      <ResponsiveContainer>
        <PieChart>
          {/* move pie's center slightly lower (cy) so it's not clipped */}
          <Pie
            data={dataWithPct}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="44%"            // moved down (was ~45% or 40% before)
            outerRadius={110}
            innerRadius={30}
            paddingAngle={2}
            labelLine={false}
            // Keep labels only for larger slices to avoid overlap
            label={({ value, name }) => (value >= 5 ? `${name} ${value}%` : null)}
          >
            {dataWithPct.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip
            formatter={(value, name, props) => {
              const datum = props.payload;
              const rawRisk = datum.risk_score ?? (datum.value * total / 100);
              return [`${(rawRisk || 0).toFixed(3)} (score)`, `${datum.name} — ${datum.value}%`];
            }}
          />

          {/* Legend placed below the chart; make it wrapped and scrollable if too long */}
          <Legend
            layout="horizontal"
            verticalAlign="bottom"
            align="center"
            iconType="square"
            iconSize={12}
            wrapperStyle={{
              marginTop: 10,
              maxHeight: 100,        // limit height of legend
              overflowY: "auto",     // scroll if too many items
              whiteSpace: "nowrap",
              display: "flex",
              justifyContent: "center",
              flexWrap: "wrap",
              gap: "8px 12px",
              padding: "4px 8px"
            }}
            formatter={(value) => {
              // value is 'B27' or 'Other' — show it cleanly
              return <span style={{ fontSize: 13 }}>{value}</span>;
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
