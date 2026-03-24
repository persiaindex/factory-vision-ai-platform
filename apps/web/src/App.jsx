import AppLayout from "./layouts/AppLayout";
import DashboardPage from "./pages/DashboardPage";
import "./styles/dashboard.css";

function App() {
  return (
    <AppLayout>
      <DashboardPage />
    </AppLayout>
  );
}

export default App;