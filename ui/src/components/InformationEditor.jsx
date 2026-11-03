const fieldLabels = {
  skill: "Kỹ năng",
  education: "Học vấn",
  experience: "Kinh nghiệm",
  certificate: "Chứng chỉ",
  project: "Dự án",
  responsibilities: "Trách nhiệm công việc",
};

export function normalizeInformation(information, fields) {
  return Object.fromEntries(
    fields.map((field) => {
      const value = information?.[field];
      if (Array.isArray(value)) return [field, value.map(String)];
      if (typeof value === "string" && value.trim()) return [field, [value]];
      return [field, []];
    }),
  );
}

export default function InformationEditor({
  title,
  information,
  onChange,
  isLoading = false,
  disabled = false,
}) {
  const fields = Object.keys(information);

  return (
    <section
      className={`information-panel${isLoading ? " is-loading" : ""}`}
      aria-label={title}
      aria-busy={isLoading}
    >
      <div className="information-panel-heading">
        <div>
          <p className="eyebrow">KIỂM TRA THÔNG TIN</p>
          <h2>{title}</h2>
        </div>
        <span className="edit-hint">Có thể chỉnh sửa</span>
      </div>
      {isLoading && (
        <div className="information-loading" role="status" aria-live="polite">
          <span className="loading-spinner" aria-hidden="true" />
          Đang cập nhật thông tin...
        </div>
      )}
      <div className="information-fields">
        {fields.map((field) => (
          <label className="information-field" key={field}>
            <span>{fieldLabels[field] ?? field}</span>
            <textarea
              rows={Math.min(6, Math.max(3, information[field].length + 1))}
              value={information[field].join("\n")}
              placeholder="Mỗi nội dung trên một dòng"
              disabled={isLoading || disabled}
              onChange={(event) =>
                onChange(
                  field,
                  event.target.value
                    .split("\n")
                    .map((item) => item.trim())
                    .filter(Boolean),
                )
              }
            />
          </label>
        ))}
      </div>
    </section>
  );
}
