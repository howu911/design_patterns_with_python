package signleton_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	signleton "01_signleton/go_signleton"
)

func TestGetInstance(t *testing.T) {
	assert.Equal(t, signleton.GetInstance(), signleton.GetInstance())
}

func BenchmarkGetInstanceParallel(b *testing.B) {
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			if signleton.GetInstance() != signleton.GetInstance() {
				b.Errorf("test fail")
			}
		}
	})
}
