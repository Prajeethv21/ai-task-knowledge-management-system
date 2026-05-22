import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { apiRequest, authHeaders } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Analytics() {
  const { token } = useAuth();
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const fetchAnalytics = async () => {
      try {
        const data = await apiRequest("/analytics", { headers: { ...authHeaders(token) } });
        if (isMounted) {
          setAnalytics(data);
        }
      } catch {
        if (isMounted) {
          setAnalytics(null);
        }
      }
    };

    fetchAnalytics();
    const intervalId = setInterval(fetchAnalytics, 10000);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, [token]);

  if (!analytics) {
    return <div>Loading analytics...</div>;
  }

  const pieData = [
    { name: "Completed", value: analytics.completed_tasks },
    { name: "Pending", value: analytics.pending_tasks }
  ];

  const barData = analytics.top_queries.map((item) => ({
    name: item.query,
    count: item.count
  }));

  return (
    <div>
      <h1>Analytics</h1>
      <div className="stat-grid">
        <div className="stat-card">
          <span className="stat-label">Total Tasks</span>
          <span className="stat-value">{analytics.total_tasks}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Completed Tasks</span>
          <span className="stat-value">{analytics.completed_tasks}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Pending Tasks</span>
          <span className="stat-value">{analytics.pending_tasks}</span>
        </div>
      </div>
      <div className="card">
        <h3>Task Distribution</h3>
        <div style={{ width: "100%", height: 260 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" outerRadius={90} fill="#0f766e" label />
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="card">
        <h3>Top Queries</h3>
        <div style={{ width: "100%", height: 280 }}>
          <ResponsiveContainer>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#1d4ed8" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
