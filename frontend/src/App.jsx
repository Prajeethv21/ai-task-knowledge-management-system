import { Routes, Route, Navigate } from "react-router-dom";
import AppLayout from "./layouts/AppLayout.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import UploadDocuments from "./pages/UploadDocuments.jsx";
import Tasks from "./pages/Tasks.jsx";
import Search from "./pages/Search.jsx";
import Analytics from "./pages/Analytics.jsx";
import { useAuth } from "./context/AuthContext.jsx";

const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="documents" element={<UploadDocuments />} />
        <Route path="tasks" element={<Tasks />} />
        <Route path="search" element={<Search />} />
        <Route path="analytics" element={<Analytics />} />
      </Route>
    </Routes>
  );
}
