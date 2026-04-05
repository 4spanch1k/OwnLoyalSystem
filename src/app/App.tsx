import { useState } from "react";
import { PublicPage } from "./components/PublicPage";
import { Dashboard } from "./components/Dashboard";
import { ServicesPage } from "./components/ServicesPage";
import { PricesPage } from "./components/PricesPage";
import { DoctorsPage } from "./components/DoctorsPage";
import { BookingPage } from "./components/BookingPage";
import { ContactsPage } from "./components/ContactsPage";
import { DoctorCabinet } from "./components/DoctorCabinet";
import { StaffLoginPage } from "./components/StaffLoginPage";
import { AnimatedPage } from "./components/motion/AnimatedPage";

export type Page =
  | "public"
  | "cabinet"
  | "staff-login"
  | "services"
  | "prices"
  | "doctors"
  | "booking"
  | "contacts"
  | "doctor-cabinet";

export default function App() {
  const [page, setPage] = useState<Page>("public");

  const nav = setPage;
  const currentPage = (() => {
    switch (page) {
      case "cabinet":
        return <Dashboard onNavigate={nav} />;
      case "staff-login":
        return <StaffLoginPage onNavigate={nav} />;
      case "services":
        return <ServicesPage onNavigate={nav} />;
      case "prices":
        return <PricesPage onNavigate={nav} />;
      case "doctors":
        return <DoctorsPage onNavigate={nav} />;
      case "booking":
        return <BookingPage onNavigate={nav} />;
      case "contacts":
        return <ContactsPage onNavigate={nav} />;
      case "doctor-cabinet":
        return <DoctorCabinet onNavigate={nav} />;
      default:
        return <PublicPage onNavigate={nav} />;
    }
  })();

  return (
    <AnimatedPage key={page}>{currentPage}</AnimatedPage>
  );
}
