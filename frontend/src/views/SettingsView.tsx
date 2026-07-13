import React from 'react';

const SettingsView: React.FC = () => {
  return (
    <div>
      <div className="dashboard-header">
        <div>
          <h1 className="header-title">Platform Settings</h1>
          <p className="header-subtitle">Manage agent behaviors, thresholds, and remote system connections</p>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">System Properties</h2>
        </div>
        <form className="settings-form" onSubmit={(e) => e.preventDefault()}>
          <div className="form-group">
            <label htmlFor="backendUrl">Backend API Server URL</label>
            <input
              type="text"
              id="backendUrl"
              className="form-control"
              defaultValue="http://127.0.0.1:8000"
            />
          </div>

          <div className="form-group">
            <label htmlFor="logPollRate">Log Polling Interval (seconds)</label>
            <input
              type="number"
              id="logPollRate"
              className="form-control"
              defaultValue="5"
            />
          </div>

          <div className="form-group">
            <label htmlFor="urgencyThreshold">Automatic Escalation Urgency Threshold</label>
            <select id="urgencyThreshold" className="form-control" defaultValue="high">
              <option value="low">Low & Above</option>
              <option value="medium">Medium & Above</option>
              <option value="high">High Only</option>
            </select>
          </div>

          <button type="submit" className="btn">Save Configurations</button>
        </form>
      </div>
    </div>
  );
};

export default SettingsView;
