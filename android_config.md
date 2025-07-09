# Android应用开发指南

本文档介绍如何为自习室管理系统开发Android应用。

## 开发方案

### 方案一：WebView混合应用（推荐）

使用Android WebView加载现有的Web界面，快速实现移动端应用。

#### 优点
- 开发成本低
- 维护简单
- 功能同步
- 快速上线

#### 关键代码示例

```java
// MainActivity.java
public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private String serverUrl = "http://your-server.com:5000";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        webView = findViewById(R.id.webview);
        setupWebView();
        webView.loadUrl(serverUrl);
    }
    
    private void setupWebView() {
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });
        
        webView.setWebChromeClient(new WebChromeClient());
    }
}
```

```xml
<!-- activity_main.xml -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

</LinearLayout>
```

#### 权限配置

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.CAMERA" />
```

### 方案二：原生Android应用

使用Kotlin/Java开发原生Android应用，通过REST API与后端通信。

#### 核心组件

1. **网络层** - Retrofit + OkHttp
2. **数据存储** - Room Database
3. **UI框架** - Android Jetpack Compose
4. **依赖注入** - Dagger-Hilt

#### 项目结构

```
app/
├── src/main/java/com/studyroom/
│   ├── data/
│   │   ├── api/          # API接口定义
│   │   ├── model/        # 数据模型
│   │   └── repository/   # 数据仓库
│   ├── ui/
│   │   ├── login/        # 登录界面
│   │   ├── main/         # 主界面
│   │   └── seat/         # 座位管理
│   └── utils/            # 工具类
```

#### API接口定义

```kotlin
// ApiService.kt
interface ApiService {
    @POST("login")
    suspend fun login(@Body loginRequest: LoginRequest): Response<LoginResponse>
    
    @GET("api/seats")
    suspend fun getSeats(): Response<List<Seat>>
    
    @PUT("api/seats/{id}")
    suspend fun updateSeat(@Path("id") id: Int, @Body seat: SeatRequest): Response<ApiResponse>
    
    @GET("api/logs")
    suspend fun getOperationLogs(): Response<List<OperationLog>>
}
```

## 功能扩展

### 1. 离线缓存

```kotlin
// 使用Room数据库缓存数据
@Entity(tableName = "seats")
data class SeatEntity(
    @PrimaryKey val id: Int,
    val seatNumber: String,
    val isOccupied: Boolean,
    val occupantName: String?,
    val cardType: String?,
    val expiryDate: String?,
    val notes: String?,
    val updatedAt: String
)
```

### 2. 条码扫描

```kotlin
// 集成ZXing条码扫描
implementation 'com.journeyapps:zxing-android-embedded:4.3.0'

// 扫描座位二维码快速定位
private fun startScan() {
    val integrator = IntentIntegrator(this)
    integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
    integrator.setPrompt("扫描座位二维码")
    integrator.setCameraId(0)
    integrator.setBeepEnabled(false)
    integrator.setBarcodeImageEnabled(true)
    integrator.initiateScan()
}
```

### 3. 推送通知

```kotlin
// Firebase Cloud Messaging
implementation 'com.google.firebase:firebase-messaging:23.0.0'

// 到期提醒推送
class StudyRoomMessagingService : FirebaseMessagingService() {
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        remoteMessage.notification?.let {
            sendNotification(it.title ?: "", it.body ?: "")
        }
    }
    
    private fun sendNotification(title: String, messageBody: String) {
        val intent = Intent(this, MainActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
        
        val pendingIntent = PendingIntent.getActivity(this, 0, intent,
            PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_IMMUTABLE)
        
        val notificationBuilder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(messageBody)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
        
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(0, notificationBuilder.build())
    }
}
```

## 构建配置

### Gradle配置

```gradle
// app/build.gradle
android {
    compileSdk 33
    
    defaultConfig {
        applicationId "com.studyroom.manager"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }
    
    buildFeatures {
        compose true
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.7.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.3.1'
    implementation 'androidx.activity:activity-compose:1.3.1'
    implementation 'androidx.compose.ui:ui:1.1.1'
    implementation 'androidx.compose.material:material:1.1.1'
    
    // Networking
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.9.0'
    
    // Database
    implementation 'androidx.room:room-runtime:2.4.2'
    implementation 'androidx.room:room-ktx:2.4.2'
    kapt 'androidx.room:room-compiler:2.4.2'
    
    // Dependency Injection
    implementation 'com.google.dagger:hilt-android:2.40.5'
    kapt 'com.google.dagger:hilt-compiler:2.40.5'
}
```

## 部署发布

### 1. 签名配置

```gradle
// 在app/build.gradle中配置签名
android {
    signingConfigs {
        release {
            storeFile file('release.keystore')
            storePassword 'your_store_password'
            keyAlias 'your_key_alias'
            keyPassword 'your_key_password'
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 2. 混淆配置

```proguard
# proguard-rules.pro
-keep class com.studyroom.manager.data.model.** { *; }
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
```

## 测试

### 单元测试

```kotlin
// SeatRepositoryTest.kt
@Test
fun `test get seats from api`() = runTest {
    val mockSeats = listOf(
        Seat(1, "A01", false, null, null, null, null, "2024-01-01")
    )
    
    whenever(apiService.getSeats()).thenReturn(Response.success(mockSeats))
    
    val result = repository.getSeats()
    
    assertEquals(mockSeats, result.getOrNull())
}
```

### UI测试

```kotlin
// MainActivityTest.kt
@Test
fun loginScreenDisplayed() {
    composeTestRule.setContent {
        StudyRoomTheme {
            LoginScreen(
                onLoginClick = { _, _ -> },
                isLoading = false
            )
        }
    }
    
    composeTestRule.onNodeWithText("用户名").assertIsDisplayed()
    composeTestRule.onNodeWithText("密码").assertIsDisplayed()
}
```

## 性能优化

1. **图片优化**: 使用WebP格式图片
2. **网络优化**: 实现请求缓存和重试机制
3. **内存优化**: 及时释放WebView资源
4. **电池优化**: 合理使用后台服务

## 安全考虑

1. **HTTPS**: 强制使用HTTPS通信
2. **证书验证**: 验证SSL证书
3. **数据加密**: 敏感数据本地加密存储
4. **代码混淆**: 发布版本启用代码混淆

这个配置指南提供了Android应用开发的完整方案，可以根据项目需求选择合适的开发方式。 