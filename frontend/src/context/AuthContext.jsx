import React, { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);

const normalizeToken = (value) => {
  if (!value || value === "null" || value === "undefined") {
    return null;
  }
  return value;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(normalizeToken(localStorage.getItem("token")));

  const login = (newToken) => {
    const normalized = normalizeToken(newToken);
    if (!normalized) {
      localStorage.removeItem("token");
      setToken(null);
      return;
    }
    localStorage.setItem("token", normalized);
    setToken(normalized);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  const value = useMemo(() => ({ token, login, logout }), [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
};
