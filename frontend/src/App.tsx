import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import { ToastProvider } from './hooks/use-toast'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import RequirementAnalyzer from './pages/RequirementAnalyzer'
import AnalysisResults from './pages/AnalysisResults'
import RequirementsLibrary from './pages/RequirementsLibrary'
import AnalysisHistory from './pages/AnalysisHistory'
import Reports from './pages/Reports'
import LearningCenter from './pages/LearningCenter'
import Settings from './pages/Settings'

export default function App() {
  return (
    <ToastProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<LandingPage />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="analyze" element={<RequirementAnalyzer />} />
          <Route path="results/:id" element={<AnalysisResults />} />
          <Route path="library" element={<RequirementsLibrary />} />
          <Route path="history" element={<AnalysisHistory />} />
          <Route path="reports" element={<Reports />} />
          <Route path="learning-center" element={<LearningCenter />} />
          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<LandingPage />} />
        </Route>
      </Routes>
    </ToastProvider>
  )
}
