import SiteHeader from "../components/SiteHeader.jsx";
import HeroSection from "../components/HeroSection.jsx";
import HowItWorks from "../components/HowItWorks.jsx";
import FeatureCard from "../components/FeatureCard.jsx";
import SiteFooter from "../components/SiteFooter.jsx";

const features = [
  {
    number: "01",
    title: "Thông tin rõ ràng",
    description:
      "Tách nội dung hồ sơ và yêu cầu công việc thành từng trường dễ theo dõi.",
  },
  {
    number: "02",
    title: "Bạn luôn làm chủ",
    description:
      "Kiểm tra và chỉnh sửa nội dung trích xuất trước khi bắt đầu đối chiếu.",
  },
  {
    number: "03",
    title: "Kết quả dễ hiểu",
    description:
      "Xem mức độ phù hợp, điểm số và lý do cho từng yêu cầu tuyển dụng.",
  },
];

export default function LandingPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <HeroSection />
        <section className="features-section section-space" aria-labelledby="features-title">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">ĐƠN GIẢN VÀ MINH BẠCH</p>
              <h2 id="features-title">Một quy trình, rõ từng bước</h2>
            </div>
            <div className="row g-4">
              {features.map((feature) => (
                <div className="col-md-4" key={feature.number}>
                  <FeatureCard {...feature} />
                </div>
              ))}
            </div>
          </div>
        </section>
        <HowItWorks />
      </main>
      <SiteFooter />
    </>
  );
}
