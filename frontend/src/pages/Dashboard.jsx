import { useEffect, useState } from "react";
import { apiRequest, authHeaders } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Dashboard() {
  const { token } = useAuth();
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const fetchDashboard = async () => {
      try {
        const data = await apiRequest("/analytics/dashboard", { headers: { ...authHeaders(token) } });
        if (isMounted) {
          setDashboard(data);
        }
      } catch {
        if (isMounted) {
          setDashboard(null);
        }
      }
    };

    fetchDashboard();
    const intervalId = setInterval(fetchDashboard, 10000);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, [token]);

  return (
    <div>
      <h1>Dashboard</h1>
      {dashboard ? (
        <>
          <div className="stat-grid">
            <div className="stat-card">
              <span className="stat-label">Total Tasks</span>
              <span className="stat-value">{dashboard.total_tasks}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Completed</span>
              <span className="stat-value">{dashboard.completed_tasks}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Pending</span>
              <span className="stat-value">{dashboard.pending_tasks}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Documents</span>
              <span className="stat-value">{dashboard.documents_count}</span>
            </div>
          </div>
          <div className="card">
            <h3>Recent Activity</h3>
            <div className="timeline">
              {dashboard.recent_activity.map((item) => (
                <div key={item.id} className="timeline-item">
                  <strong>{item.user_email || `User ${item.user_id}`}</strong>
                  <span>{item.action}</span>
                  <span className="stat-label">{item.details}</span>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        <div className="card">Loading dashboard...</div>
      )}
    </div>
  );
}
