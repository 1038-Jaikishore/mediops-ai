import React from 'react';
import { Activity, AlertTriangle, CheckCircle, Database } from 'lucide-react';

const HomeView: React.FC = () => {
  return (
    <div>
      <div className="dashboard-header">
        <div>
          <h1 className="header-title">System Overview</h1>
          <p className="header-subtitle">Real-time status of hospital systems and AI Operations agents</p>
        </div>
        <div className="status-indicator">
          <span className="status-dot"></span>
          All Agents Active
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="stats-card">
          <div className="stats-info">
            <h3>Active Incidents</h3>
            <div className="value">4</div>
          </div>
          <div className="stats-icon-container error-theme">
            <AlertTriangle size={24} />
          </div>
        </div>

        <div className="stats-card">
          <div className="stats-info">
            <h3>Resolved (24h)</h3>
            <div className="value">18</div>
          </div>
          <div className="stats-icon-container cyan-theme">
            <CheckCircle size={24} />
          </div>
        </div>

        <div className="stats-card">
          <div className="stats-info">
            <h3>Logs Analyzed</h3>
            <div className="value">14,289</div>
          </div>
          <div className="stats-icon-container blue-theme">
            <Activity size={24} />
          </div>
        </div>

        <div className="stats-card">
          <div className="stats-info">
            <h3>RAG Knowledge Base</h3>
            <div className="value">124 docs</div>
          </div>
          <div className="stats-icon-container purple-theme">
            <Database size={24} />
          </div>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">Active AI Agents</h2>
        </div>
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Agent Name</th>
                <th>Status</th>
                <th>Role/Focus</th>
                <th>Last Decision</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={{ fontWeight: 600 }}>Triage Agent</td>
                <td><span className="badge badge-resolved">Idle</span></td>
                <td>Incident Intake & Urgency Rating</td>
                <td>Classified Laboratory API latency as HIGH</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 600 }}>Root Cause Agent</td>
                <td><span className="badge badge-triage">Analyzing</span></td>
                <td>Log Analysis & Error Detection</td>
                <td>Scanning appointment microservice trace logs...</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 600 }}>Action Agent</td>
                <td><span className="badge badge-resolved">Idle</span></td>
                <td>System Remediation & Scripts</td>
                <td>Initiated replica failover for Billing DB</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 600 }}>Verification Agent</td>
                <td><span className="badge badge-resolved">Idle</span></td>
                <td>Post-action metric assessment</td>
                <td>Verified laboratory endpoint response speed under 120ms</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default HomeView;
