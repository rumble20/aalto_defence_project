import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  serverExternalPackages: [],
  experimental: {
    turbo: {
      root: process.cwd(),
    },
  },
};

export default nextConfig;
