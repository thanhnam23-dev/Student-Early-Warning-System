# ROC Comparison

ROC comparison được sử dụng để đánh giá và so sánh khả năng phân biệt giữa các lớp của các mô hình trên tập kiểm thử độc lập. Đường cong ROC biểu diễn mối quan hệ giữa **True Positive Rate (TPR)** và **False Positive Rate (FPR)** ở nhiều ngưỡng phân loại khác nhau, trong khi diện tích dưới đường cong (**Area Under the Curve - AUC**) phản ánh hiệu quả phân loại tổng thể của mô hình. Mô hình có đường ROC nằm gần góc trên bên trái hơn và giá trị AUC cao hơn được xem là có khả năng phân loại tốt hơn. Biểu đồ này cung cấp bằng chứng trực quan để so sánh hiệu năng giữa các thuật toán và hỗ trợ lựa chọn mô hình phù hợp.

---

# Validation Accuracy Comparison

Biểu đồ **Validation Accuracy Across Epochs** thể hiện sự thay đổi của độ chính xác trên tập validation trong suốt quá trình huấn luyện của các mô hình. Hình này được sử dụng để đánh giá **tốc độ hội tụ**, **khả năng học** và **độ ổn định** của từng thuật toán. Một mô hình tốt thường đạt độ chính xác cao sau một số lượng epoch hợp lý và duy trì đường cong ổn định, ít dao động. Việc so sánh các đường cong validation accuracy giúp quan sát trực quan sự khác biệt về quá trình tối ưu giữa các mô hình.

---

# Validation Loss Comparison

Biểu đồ **Validation Loss Across Epochs** mô tả sự thay đổi của hàm mất mát trên tập validation trong quá trình huấn luyện. Giá trị loss phản ánh mức sai số của mô hình, do đó loss càng giảm và ổn định thì mô hình càng hội tụ tốt. Hình này được sử dụng để đánh giá khả năng tối ưu của từng thuật toán, đồng thời hỗ trợ phát hiện các hiện tượng như **hội tụ chậm**, **dao động mạnh** hoặc **quá khớp (overfitting)** nếu validation loss bắt đầu tăng trong khi quá trình huấn luyện vẫn tiếp tục.

---

# Learning Curves (Training vs Validation)

Biểu đồ **Learning Curves** trình bày đồng thời sự thay đổi của **Training Loss**, **Validation Loss**, **Training Accuracy** và **Validation Accuracy** theo số lượng epoch trong quá trình huấn luyện của một mô hình. Đây là công cụ quan trọng để phân tích hành vi học của mô hình, đánh giá khả năng hội tụ cũng như mức độ tổng quát hóa trên dữ liệu chưa quan sát. Khi khoảng cách giữa đường huấn luyện và đường validation nhỏ, đồng thời cả hai cùng hội tụ ổn định, điều đó cho thấy mô hình học hiệu quả và có khả năng tổng quát hóa tốt. Ngược lại, nếu hai đường tách xa nhau hoặc hiệu năng trên tập validation suy giảm trong khi hiệu năng trên tập huấn luyện vẫn tiếp tục cải thiện, đây là dấu hiệu của hiện tượng **overfitting**.