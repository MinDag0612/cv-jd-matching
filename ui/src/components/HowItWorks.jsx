const steps = [
  {
    number: "1",
    title: "Gửi CV và JD",
    description: "Bắt đầu với hồ sơ ứng viên và mô tả công việc cần đối chiếu.",
  },
  {
    number: "2",
    title: "Kiểm tra thông tin",
    description: "Xem lại nội dung được trích xuất và chỉnh sửa khi cần thiết.",
  },
  {
    number: "3",
    title: "Xem kết quả phù hợp",
    description: "Nhận điểm số, phân tích từng yêu cầu và kết luận tổng quan.",
  },
];

export default function HowItWorks() {
  return (
    <section className="process-section section-space" id="quy-trinh">
      <div className="container">
        <div className="section-heading">
          <p className="eyebrow">TỪ HỒ SƠ ĐẾN GÓC NHÌN</p>
          <h2 id="process-title">Ba bước để nhìn thấy sự phù hợp</h2>
        </div>
        <div className="row g-4" aria-labelledby="process-title">
          {steps.map((step) => (
            <div className="col-md-4" key={step.number}>
              <article className="process-step">
                <span className="step-number">{step.number}</span>
                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </article>
            </div>
          ))}
        </div>
        <p className="process-note">
          Đây là trang giới thiệu. Luồng tải hồ sơ và xem kết quả sẽ được bổ sung
          ở bước tiếp theo.
        </p>
      </div>
    </section>
  );
}
