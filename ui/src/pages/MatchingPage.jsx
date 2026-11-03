import { useState } from "react";
import FileUploadCard from "../components/FileUploadCard.jsx";
import InformationEditor, {
  normalizeInformation,
} from "../components/InformationEditor.jsx";
import MatchResults from "../components/MatchResults.jsx";
import { compareInformation, extractFile } from "../services/matchingApi.js";

const resumeFields = ["skill", "education", "experience", "certificate", "project"];
const jobFields = ["skill", "education", "experience", "certificate", "responsibilities"];

function emptyInformation(fields) {
  return Object.fromEntries(fields.map((field) => [field, []]));
}

export default function MatchingPage({ onBack }) {
  const [files, setFiles] = useState({ resume: null, job: null });
  const [information, setInformation] = useState({ resume: null, job: null });
  const [extracting, setExtracting] = useState({ resume: false, job: false });
  const [fileErrors, setFileErrors] = useState({ resume: "", job: "" });
  const [compareError, setCompareError] = useState("");
  const [isComparing, setIsComparing] = useState(false);
  const [result, setResult] = useState(null);
  const isExtracting = extracting.resume || extracting.job;

  const canCompare =
    information.resume &&
    information.job &&
    resumeFields.some((field) => {
      const jobField = field === "project" ? "responsibilities" : field;
      return information.resume[field]?.length && information.job[jobField]?.length;
    });

  function handleFileChange(role, file) {
    if (isComparing || extracting[role]) return;
    setFiles((current) => ({ ...current, [role]: file }));
    setInformation((current) => ({ ...current, [role]: null }));
    setFileErrors((current) => ({ ...current, [role]: "" }));
    setCompareError("");
    setResult(null);
  }

  async function handleExtract(role) {
    const file = files[role];
    if (!file || extracting[role] || isComparing) return;

    const fields = role === "resume" ? resumeFields : jobFields;
    setExtracting((current) => ({ ...current, [role]: true }));
    setFileErrors((current) => ({ ...current, [role]: "" }));
    setCompareError("");
    setResult(null);

    try {
      const response = await extractFile(file, role === "resume");
      if (!response.information || typeof response.information !== "object") {
        throw new Error("Máy chủ không trả về thông tin trích xuất hợp lệ.");
      }
      setInformation((current) => ({
        ...current,
        [role]: normalizeInformation(response.information, fields),
      }));
    } catch (error) {
      setFileErrors((current) => ({ ...current, [role]: error.message }));
    } finally {
      setExtracting((current) => ({ ...current, [role]: false }));
    }
  }

  function handleInformationChange(role, field, value) {
    if (isComparing || extracting[role]) return;
    setInformation((current) => ({
      ...current,
      [role]: { ...current[role], [field]: value },
    }));
    setResult(null);
    setCompareError("");
  }

  async function handleCompare(event) {
    event.preventDefault();
    if (!canCompare || isComparing || isExtracting) return;

    const cvData = {
      ...emptyInformation(resumeFields),
      ...information.resume,
    };
    const jdData = {
      ...emptyInformation(jobFields),
      ...information.job,
    };

    setIsComparing(true);
    setCompareError("");
    setResult(null);

    try {
      const response = await compareInformation(cvData, jdData);
      if (typeof response.total_score !== "number" || !response.list_commend) {
        throw new Error("Máy chủ trả về kết quả đối chiếu không hợp lệ.");
      }
      setResult(response);
    } catch (error) {
      setCompareError(error.message);
    } finally {
      setIsComparing(false);
    }
  }

  return (
    <main className="matching-page">
      <header className="matching-header">
        <div className="container matching-header-inner">
          <button className="brand-mark" type="button" onClick={onBack} aria-label="Về trang chủ">
            CV <span>x</span> JD
          </button>
          <button className="back-link" type="button" onClick={onBack}>
            ← Trang giới thiệu
          </button>
        </div>
      </header>

      <div className="container matching-content">
        <div className="matching-intro">
          <p className="eyebrow">ĐỐI CHIẾU CV VỚI CÔNG VIỆC</p>
          <h1>Tìm điểm chung, hiểu điểm khác biệt.</h1>
          <p>
            Tải CV và mô tả công việc. Kiểm tra thông tin được trích xuất, chỉnh sửa nếu cần,
            rồi bắt đầu phân tích.
          </p>
        </div>

        <div className="upload-grid">
          <FileUploadCard
            role="resume"
            title="Hồ sơ ứng viên"
            description="Tải CV cần đánh giá"
            file={files.resume}
            information={information.resume}
            isExtracting={extracting.resume}
            isComparing={isComparing}
            error={fileErrors.resume}
            onFileChange={(file) => handleFileChange("resume", file)}
            onExtract={() => handleExtract("resume")}
          />
          <FileUploadCard
            role="job"
            title="Mô tả công việc"
            description="Tải JD của vị trí tuyển dụng"
            file={files.job}
            information={information.job}
            isExtracting={extracting.job}
            isComparing={isComparing}
            error={fileErrors.job}
            onFileChange={(file) => handleFileChange("job", file)}
            onExtract={() => handleExtract("job")}
          />
        </div>

        {(information.resume || information.job) && (
          <div className="editors-grid">
            {information.resume && (
              <InformationEditor
                title="Thông tin hồ sơ"
                information={information.resume}
                isLoading={extracting.resume}
                disabled={isComparing}
                onChange={(field, value) => handleInformationChange("resume", field, value)}
              />
            )}
            {information.job && (
              <InformationEditor
                title="Thông tin công việc"
                information={information.job}
                isLoading={extracting.job}
                disabled={isComparing}
                onChange={(field, value) => handleInformationChange("job", field, value)}
              />
            )}
          </div>
        )}

        <form className="compare-action" onSubmit={handleCompare}>
          <button
            className="btn btn-ink compare-button"
            type="submit"
            disabled={!canCompare || isComparing || isExtracting}
            aria-busy={isComparing}
          >
            {isComparing && <span className="loading-spinner" aria-hidden="true" />}
            {isComparing ? "Đang phân tích..." : "So sánh hồ sơ"}
          </button>
          {!canCompare && (
            <p>
              Hãy trích xuất cả hai tài liệu và đảm bảo có ít nhất một nhóm thông tin để đối chiếu.
            </p>
          )}
          {isComparing && (
            <p className="compare-wait" role="status" aria-live="polite">
              Quá trình phân tích có thể mất khoảng 3–4 phút. Vui lòng giữ trang này mở.
            </p>
          )}
          {compareError && (
            <p className="form-error compare-error" role="alert">
              {compareError}
            </p>
          )}
        </form>

        {result && <MatchResults result={result} />}
      </div>
    </main>
  );
}
