# Branch ve Pull Request Silme Rehberi (Main Branch Hariç)

Bu rehber, 'main' branchi dışındaki Git branchlerini ve Pull Request'lerini (PR) güvenli bir şekilde silme adımlarını, potansiyel riskleri, en iyi uygulamaları ve silme işlemlerinin nasıl doğrulanacağını açıklamaktadır.

## 1. Giriş

Depo temizliği, daha düzenli ve yönetilebilir bir proje geçmişi sağlar. Bu işlem, artık aktif olarak geliştirilmeyen veya birleştirilmiş (merged) branchlerin ve kapatılmış/birleştirilmiş PR'ların temizlenmesini içerir. **Bu işlemler geri alınamaz olduğundan dikkatli yapılmalıdır.**

## 2. Potansiyel Riskler

*   **Veri Kaybı:** Henüz birleştirilmemiş veya önemli değişiklikler içeren bir branchin silinmesi veri kaybına yol açabilir.
*   **İş Akışı Kesintisi:** Aktif olarak kullanılan bir branchin yanlışlıkla silinmesi, diğer geliştiricilerin iş akışını bozabilir.
*   **Tarihçe Kaybı:** Silinen bir branchin commit geçmişi, eğer başka bir branch tarafından referans alınmıyorsa kaybolabilir.

## 3. En İyi Uygulamalar

*   **Yedekleme:** Kritik bir silme işlemi yapmadan önce depoyu yedeklemeyi düşünebilirsiniz.
*   **İletişim:** Özellikle paylaşılan bir depoda çalışıyorsanız, silme işlemlerini diğer ekip üyeleriyle önceden görüşün.
*   **Onay:** Bir branchi silmeden önce, içerdiği tüm değişikliklerin 'main' branchine birleştirildiğinden veya artık ihtiyaç duyulmadığından emin olun.
*   **Aşamalı Silme:** Birden fazla branch silinecekse, bunları küçük gruplar halinde silmek ve her adımda doğrulamak daha güvenlidir.

## 4. Branch Silme Adımları

Bu adımlar hem yerel (local) hem de uzak (remote) branchleri kapsar. `main` branchini silmemeye özellikle dikkat edin.

### 4.1. Yerel Branchleri Tespit Etme

`main` branchi dışındaki yerel branchleri listelemek için:

```bash
git branch | grep -v 