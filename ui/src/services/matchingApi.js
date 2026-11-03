const COMPARE_TIMEOUT_MS = 10 * 60 * 1000;

async function requestJson(url, options, timeoutMs) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    const responseText = await response.text();
    let payload;

    try {
      payload = responseText ? JSON.parse(responseText) : {};
    } catch {
      throw new Error("Máy chủ trả về dữ liệu không hợp lệ.");
    }

    if (!response.ok) {
      throw new Error(
        payload.mess || payload.detail || `Yêu cầu thất bại (${response.status}).`,
      );
    }

    return payload;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("Yêu cầu đã quá thời gian chờ. Vui lòng thử lại.");
    }
    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export function extractFile(file, isResume) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("is_resume", String(isResume));

  return requestJson(
    "/extractor/extract-file",
    { method: "POST", body: formData },
    COMPARE_TIMEOUT_MS,
  );
}

export function compareInformation(cvData, jdData) {
  return requestJson(
    "/extractor/compare",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cv_data: cvData, jd_data: jdData }),
    },
    COMPARE_TIMEOUT_MS,
  );
}
