package observer

import "fmt"

type ISubject interface {
	Register(observer IObserver)
	Remove(observer IObserver)
	Notify(msg string)
}

type IObserver interface {
	Update(msg string)
}

type Subject struct {
	observers []IObserver
}

func (sub *Subject) Register(observer IObserver) {
	sub.observers = append(sub.observers, observer)
}

func (sub *Subject) Remove(observer IObserver) {
	for i, ob := range sub.observers {
		if ob == observer {
			sub.observers = append(sub.observers[:i], sub.observers[i+1:]...)
		}
	}
}

func (sub *Subject) Notify(msg string) {
	for _, ob := range sub.observers {
		ob.Update(msg)
	}
}

type Oberserver struct{}

// Observer1 Observer1
type Observer1 struct{}

// Update 实现观察者接口
func (Observer1) Update(msg string) {
	fmt.Println("Observer1: ", msg)
}

// Observer2 Observer2
type Observer2 struct{}

// Update 实现观察者接口
func (Observer2) Update(msg string) {
	fmt.Println("Observer2: ", msg)
}
