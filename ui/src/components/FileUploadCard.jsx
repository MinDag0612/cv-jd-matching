import { useRef } from "react";

export default function FileUploadCard({
  role,
  title,
  description,
  file,
  information,
  isExtracting,
  isComparing,
  error,
  onFileChange,
  onExtract,
}) {
  const inputRef = useRef(null);
  const isReady = Boolean(information);
  const inputId = `${role}-file`;
  const isBusy = isExtracting || isComparing;

  function handleChange(event) {
    const selectedFile = event.target.files?.[0] ?? null;
    if (selectedFile) onFileChange(selectedFile);
    event.target.value = "";
  }

  function handleDrop(event) {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files?.[0];
    if (droppedFile && !isBusy) onFileChange(droppedFile);
  }

  return (
    <section
      className={`upload-card upload-card-${role}${file ? " has-file" : ""}${isReady ? " has-information" : ""}`}
      aria-labelledby={`${role}-title`}
      aria-busy={isExtracting}
    >
      <div className="upload-card-heading">
        <span className="upload-step">{role === "resume" ? "01" : "02"}</span>
        <div>
          <h2 id={`${role}-title`}>{title}</h2>
          <p>{description}</p>
        </div>
      </div>
      <input
        ref={inputRef}
        id={inputId}
        className="visually-hidden"
        type="file"
        disabled={isBusy}
        accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        onChange={handleChange}
      />
      <button
        className="file-dropzone"
        type="button"
        disabled={isBusy}
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
        aria-describedby={`${role}-file-help`}
      >
        <span className="file-dropzone-icon" aria-hidden="true">
          {file ? "✓" : "↑"}
        </span>
        <strong>{file?.name ?? "Chọn hoặc thả tệp tại đây"}</strong>
        {file && <span className="file-selected-label">Đã nhận tệp</span>}
        <span id={`${role}-file-help`}>Hỗ trợ định dạng PDF và DOCX</span>
      </button>
      <div className="upload-card-footer">
        <span
          className={`extract-state${file ? " has-file-state" : ""}${isReady ? " is-ready" : ""}`}
          aria-live="polite"
        >
          {isExtracting
            ? "Đang trích xuất thông tin..."
            : isReady
              ? "Đã trích xuất · Có thể chỉnh sửa bên dưới"
              : "Chưa có thông tin"}
        </span>
        <button
          className={`btn btn-outline-ink extract-button${file ? " has-file" : ""}${isReady ? " is-ready" : ""}`}
          type="button"
          disabled={!file || isBusy}
          aria-busy={isExtracting}
          onClick={onExtract}
        >
          {isExtracting && <span className="loading-spinner" aria-hidden="true" />}
          {isExtracting ? "Đang xử lý..." : isReady ? "Trích xuất lại" : "Trích xuất"}
        </button>
      </div>
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
    </section>
  );
}
