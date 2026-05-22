import { useEffect, useState } from "react";
import { apiRequest, authHeaders } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function UploadDocuments() {
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("success");
  const [dragging, setDragging] = useState(false);
  const [progress, setProgress] = useState(0);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const { token } = useAuth();

  const loadDocuments = async () => {
    try {
      const data = await apiRequest("/documents", { headers: { ...authHeaders(token) } });
      setDocuments(data);
    } catch {
      setDocuments([]);
    }
  };

  const handleUpload = async () => {
    setMessage("");
    if (!file) {
      setMessageType("error");
      setMessage("Select a .txt file first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    try {
      setProgress(10);
      const timer = setInterval(() => {
        setProgress((prev) => (prev >= 90 ? prev : prev + 10));
      }, 200);
      const data = await apiRequest("/documents", {
        method: "POST",
        headers: { ...authHeaders(token) },
        body: formData
      });
      clearInterval(timer);
      setProgress(100);
      setMessageType("success");
      setMessage(`Uploaded ${data.original_name}`);
      setTimeout(() => setProgress(0), 600);
      loadDocuments();
    } catch (err) {
      setMessageType("error");
      setMessage(err.message);
      setProgress(0);
    }
  };

  const confirmDelete = async () => {
    if (!deleteTarget) return;
    try {
      await apiRequest(`/documents/${deleteTarget.id}`, {
        method: "DELETE",
        headers: { ...authHeaders(token) }
      });
      setMessageType("success");
      setMessage(`Deleted ${deleteTarget.original_name}`);
      setDeleteTarget(null);
      loadDocuments();
    } catch (err) {
      setMessageType("error");
      setMessage(err.message);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, [token]);

  return (
    <div>
      <h1>Upload Documents</h1>
      <div className="card">
        <div
          className={`dropzone ${dragging ? "dragging" : ""}`}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(event) => {
            event.preventDefault();
            setDragging(false);
            const droppedFile = event.dataTransfer.files[0];
            if (droppedFile) {
              setFile(droppedFile);
            }
          }}
        >
          <p>{file ? `Selected: ${file.name}` : "Drag & drop a .txt file here"}</p>
          <input type="file" accept=".txt" onChange={(event) => setFile(event.target.files[0])} />
          <button onClick={handleUpload}>Upload</button>
        </div>
        {progress > 0 ? (
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        ) : null}
        {message ? <div className={`toast ${messageType}`}>{message}</div> : null}
      </div>
      <div className="card">
        <h3>Uploaded Documents</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Filename</th>
              <th>Uploaded At</th>
              <th>Size</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.original_name}</td>
                <td>{new Date(doc.uploaded_at).toLocaleString()}</td>
                <td>{doc.size} bytes</td>
                <td>
                  <button className="secondary" onClick={() => setDeleteTarget(doc)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {documents.length === 0 ? <div className="empty-state">No documents yet.</div> : null}
      </div>
      {deleteTarget ? (
        <div className="modal-backdrop">
          <div className="modal">
            <h3>Delete document?</h3>
            <p>This will remove {deleteTarget.original_name} and rebuild the index.</p>
            <div className="form-row">
              <button onClick={confirmDelete}>Confirm</button>
              <button className="secondary" onClick={() => setDeleteTarget(null)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
