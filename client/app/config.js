var config;
if (process.env.NODE_ENV === "development") {
  config = {
    apiUrl: "http://0.0.0.0:6543"
  };
} else if (process.env.NODE_ENV === "production") {
  config = {
    apiUrl: "/api"
  };
}

module.exports = config;
