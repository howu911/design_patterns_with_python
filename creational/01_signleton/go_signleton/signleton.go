package signleton

// Singleton 饿汉式单例
type Singleton struct{}

var singleton *Singleton

func GetInstance() *Singleton {
	return singleton
}
