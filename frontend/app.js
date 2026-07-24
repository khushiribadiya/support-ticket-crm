const API_BASE = "/api/tickets";

function showToast(message, isError = false) {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.className =
    "fixed bottom-5 right-5 px-4 py-3 rounded-lg shadow-lg text-white text-sm z-50 " +
    (isError ? "bg-red-500" : "bg-green-600");
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

function statusBadgeClass(status) {
  if (status === "Open") return "bg-red-100 text-red-700";
  if (status === "In Progress") return "bg-yellow-100 text-yellow-700";
  if (status === "Closed") return "bg-green-100 text-green-700";
  return "bg-gray-100 text-gray-700";
}

function formatDate(isoString) {
  const utcString = isoString.endsWith("Z") ? isoString : isoString + "Z";
  const d = new Date(utcString);
  return d.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
