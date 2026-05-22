import { useEffect, useState } from "react";
import { apiRequest, authHeaders } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Tasks() {
  const { token } = useAuth();
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [status, setStatus] = useState("");
  const [assignedTo, setAssignedTo] = useState("");
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    title: "",
    description: "",
    assigned_to: "",
    status: "pending"
  });

  const loadTasks = async () => {
    const params = new URLSearchParams();
    if (status) params.append("status", status);
    if (assignedTo) params.append("assigned_to", assignedTo);
    const data = await apiRequest(`/tasks?${params.toString()}`, {
      headers: { ...authHeaders(token) }
    });
    setTasks(data);
  };

  useEffect(() => {
    const init = async () => {
      await loadTasks();
      try {
        const me = await apiRequest("/users/me", { headers: { ...authHeaders(token) } });
        setCurrentUser(me);
        if (me?.role_name === "Admin") {
          const data = await apiRequest("/users", { headers: { ...authHeaders(token) } });
          setUsers(data);
        }
      } catch {
        setCurrentUser(null);
      }
    };

    init();
  }, [token]);

  const handleCreate = async (event) => {
    event.preventDefault();
    setMessage("");
    try {
      await apiRequest("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders(token) },
        body: JSON.stringify({
          title: form.title,
          description: form.description || null,
          assigned_to: Number(form.assigned_to),
          status: form.status
        })
      });
      setMessage("Task created");
      setForm({ title: "", description: "", assigned_to: "", status: "pending" });
      loadTasks();
    } catch (err) {
      setMessage(err.message);
    }
  };

  const updateStatus = async (taskId, newStatus) => {
    setMessage("");
    try {
      await apiRequest(`/tasks/${taskId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders(token) },
        body: JSON.stringify({ status: newStatus })
      });
      setMessage("Task updated");
      loadTasks();
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div>
      <h1>Tasks</h1>
      {currentUser?.role_name === "Admin" ? (
        <div className="card">
          <h3>Create Task</h3>
          <form onSubmit={handleCreate}>
            <div className="form-row">
              <input
                placeholder="Title"
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
                required
              />
              <input
                placeholder="Description"
                value={form.description}
                onChange={(event) => setForm({ ...form, description: event.target.value })}
              />
              <select
                value={form.assigned_to}
                onChange={(event) => setForm({ ...form, assigned_to: event.target.value })}
                required
              >
                <option value="">Assign To</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.email} ({user.role_name || user.role_id})
                  </option>
                ))}
              </select>
              <select
                value={form.status}
                onChange={(event) => setForm({ ...form, status: event.target.value })}
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
              <button type="submit">Create</button>
            </div>
          </form>
        </div>
      ) : null}
      <div className="card">
        <div className="form-row">
          <select value={status} onChange={(event) => setStatus(event.target.value)}>
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
          <input
            placeholder="Assigned To (user id)"
            value={assignedTo}
            onChange={(event) => setAssignedTo(event.target.value)}
          />
          <button onClick={loadTasks}>Apply Filters</button>
        </div>
        {message ? <div>{message}</div> : null}
        <table className="table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Status</th>
              <th>Assigned To</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id}>
                <td>{task.title}</td>
                <td>
                  <span className={`status-badge status-${task.status}`}>
                    {task.status.replace("_", " ")}
                  </span>
                </td>
                <td>
                  {users.find((user) => user.id === task.assigned_to)?.email || task.assigned_to}
                </td>
                <td>
                  <select
                    value={task.status}
                    onChange={(event) => updateStatus(task.id, event.target.value)}
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {tasks.length === 0 ? <div className="empty-state">No tasks found.</div> : null}
      </div>
    </div>
  );
}
