/** @type {import('next').NextConfig} */
const ciApiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "";

if (process.env.CI && !ciApiBaseUrl) {
  throw new Error(
    "Missing NEXT_PUBLIC_API_BASE_URL for CI build. Set it to http://127.0.0.1:8000."
  );
}

const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
