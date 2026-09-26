import { ImageResponse } from "next/og";

export const size = { width: 32, height: 32 };
export const contentType = "image/png";

export default function Icon() {
  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#1f4d3a",
        color: "#f4f1ea",
        fontSize: 18,
        fontFamily: "serif",
      }}
    >
      E
    </div>,
    size,
  );
}
