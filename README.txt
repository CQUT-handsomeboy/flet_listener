推流地址 rtsp://localhost:8554/mystream

实现了播放视频与音频、断流重连。

/**********重点**********/
WhisperLive Client未提供API重定向输出结果，需要对包的源码进行修改。