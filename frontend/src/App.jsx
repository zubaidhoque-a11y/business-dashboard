import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
  PieChart, Pie, Cell, Legend, ResponsiveContainer,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000";
const COLORS = ["#4f46e5", "#06b6d4", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6", "#ec4899", "#64748b"];

function useData(path, initial = []) {
  const [data, setData] = useState(initial);
  const [error, setError] = useState("");
  useEffect(() => {
    fetch(`${API}${path}`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => setError("Could not load data. Is the backend running?"));
  }, [path]);
  return { data, error };
}

function BarCard({ title, path, labelKey }) {
  const { data, error } = useData(path);
  return (
    <div className="card">
      <h2>{title}</h2>
      {error && <p className="error">{error}</p>}
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={labelKey} interval={0} angle={-25} textAnchor="end" height={70} />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#4f46e5" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function PieCard({ title, path, labelKey }) {
  const { data, error } = useData(path);
  return (
    <div className="card">
      <h2>{title}</h2>
      {error && <p className="error">{error}</p>}
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie data={data} dataKey="count" nameKey={labelKey} outerRadius={100} label>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function App() {
  const { data: totalData } = useData("/stats/total", {});
  return (
    <div className="container">
      <h1>Business Listings Dashboard</h1>
      <p className="subtitle">Aggregated view of scraped business data</p>
      <div className="total">Total listings: {totalData.total ?? "..."}</div>
      <div className="grid">
        <BarCard title="City-wise Count" path="/stats/city" labelKey="city" />
        <BarCard title="Category-wise Count" path="/stats/category" labelKey="category" />
        <PieCard title="Source-wise Count" path="/stats/source" labelKey="source" />
      </div>
    </div>
  );
}
