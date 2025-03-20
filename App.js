import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

import Main from './layout/components/Main';
import AuditRequestForm from './services/AuditRequest/AuditRequestForm';
import Plan from './services/Plan/Plan';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/request" element={<AuditRequestForm />} />
          <Route path="/plan" element={<Plan />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
