import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { LayoutDashboard, AlertOctagon, Terminal, Settings as SettingsIcon } from 'lucide-react';
import HomeView from './views/HomeView';
import IncidentsView from './views/IncidentsView';
import LogsView from './views/LogsView';
import SettingsView from './views/SettingsView';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="app-container">
        {/* Sidebar Panel */}
        <aside className="sidebar">
          <div className="logo-container">
            <div className="logo-icon">M</div>
            <span className="logo-text">MediOps AI</span>
          </div>

          <nav>
            <ul className="nav-links">
              <li>
                <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} end>
                  <LayoutDashboard size={18} />
                  <span>Dashboard</span>
                </NavLink>
              </li>
              <li>
                <NavLink to="/incidents" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                  <AlertOctagon size={18} />
                  <span>Incidents</span>
                </NavLink>
              </li>
              <li>
                <NavLink to="/logs" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                  <Terminal size={18} />
                  <span>Logs Stream</span>
                </NavLink>
              </li>
              <li>
                <NavLink to="/settings" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                  <SettingsIcon size={18} />
                  <span>Settings</span>
                </NavLink>
              </li>
            </ul>
          </nav>
        </aside>

        {/* Main Operational Panel */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomeView />} />
            <Route path="/incidents" element={<IncidentsView />} />
            <Route path="/logs" element={<LogsView />} />
            <Route path="/settings" element={<SettingsView />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
