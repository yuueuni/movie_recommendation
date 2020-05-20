# Django PJT5
* Ajax 이용한 좋아요 기능 구현 및 영화 추천 알고리즘 적용
> [github](https://github.com/yuueuni/movie_recommendation)

## git
* 로컬 환경과 git branch 익숙해지기 위해 로컬 도전

### virtualenv
```bash
$ pip install virtualenv # 가상환경 라이브러리 ?
$ python -m venv venv # 가상환경 venv 구축
$ source venv/Scripts/activate # 가상환경 활성화
# .. pip install django 등 필요한 라이브러리 설치
$ pip freeze > requirements.txt # 버전 저장
$ pip install -r requirements.txt
```

### git branch
* git repo 생성 후 collaborator 추가
* 각자 branch 생성 후 작업 후 `git push [remote_name] [branch_name]` 후 pull request
* 이때 브랜치 아닌 **master**로 push 할 경우 repo에 직접 push 되어짐 (모든 collaborator) > 브랜치로 push 주의

* 로컬로 진행하고 싶었으나 cs50으로 다시 작업했음
> 가상환경 생성 실패 및 git 미숙으로 인해

## ajax
```html
<!-- 'base.html' axios CDN -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

<!-- detail.html -->
<!-- 로그인된 유저가 `좋아요` 누른 경우 -->
{% if request.user in movie.like_user.all %}
  <i class="fas fa-heart fa-lg like-buttons" style="color:crimson" data-id="{{ movie.pk }}"></i>
{% else %}
  <i class="fas fa-heart fa-lg like-buttons" style="color:black" data-id="{{ movie.pk }}"></i>
{% endif %}


<script>
  const likeButtonList = document.querySelectorAll('.like-buttons')

  likeButtonList.forEach(likeButton => {
    likeButton.addEventListener('click', e => {
      const movidID = e.target.dataset.id

      // 로그인 확인
      {% if user.is_authenticated %}
      axios.get(`/movies/${movidID}/movie_like/`)
      .then(res => {
          document.querySelector(`#like-count-${movidID}`).innerText = res.data.count
          if (res.data.liked) {
            e.target.style.color = 'crimson'
          } else {
            e.target.style.color = 'black'
          }
        })
      {% else %}
        alert('로그인이 필요합니다.')
      {% endif %}
    })
  })
</script>
```
```python

def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_user.filter(pk=user.pk).exists():
        movie.like_user.remove(user)
        liked = False
    else:
        movie.like_user.add(user)
        liked = True
    context = {
        'liked': liked,
        'count': movie.like_user.count()
    }
    return JsonResponse(context)
```

### 기존 django 활용
```html
{% if request.user.is_authenticated %}
    {% if request.user in review.like_user.all %}
        <p class="mb-0"><a href="{% url 'community:review_like' movie.pk review.pk %}"><i class="fas fa-heart fa-lg" style="color:crimson;"></i></a> {{ review.like_user.count }}명이 좋아합니다.</p>
    {% else %}
        <p class="mb-0"><a href="{% url 'community:review_like' movie.pk review.pk %}"><i class="far fa-heart fa-lg" style="color:crimson;"></i></a> {{ review.like_user.count }}명이 좋아합니다.</p>
    {% endif %}
{% else %}
<p class="mb-0"><i class="far fa-heart fa-lg" style="color:crimson;"></i> {{ review.like_user.count }}명이 좋아합니다.</p>
{% endif %}
```
```python
def review_like(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_user.filter(id=request.user.pk).exists():
        review.like_user.remove(request.user)
    else:
        review.like_user.add(request.user)
    return redirect('community:review_detail', movie_pk, review.pk)
```

* django와 ajax 코드 비슷해 보이지만 ajax 활용시 페이지 재로딩 없이 (새로고침없이) 비동기처리

* [ajax MDN](https://developer.mozilla.org/ko/docs/Web/Guide/AJAX)
    * 입력값 주고받는 로직 연습 필요
    * 다양한 event 연습 및 찾아보기 (ex. click, mouseover 등)

## loaddata
```bash
$ python manage.py loaddata [파일명]
```
* 이때 해당 파일은 해당 앱 하위 폴더에 위치 (ex. movies/fixtures/moviedata.json)
* 터미널은 프로젝트 위치에서 (해당 앱 아님)

### 오류발생
* model - Movie에서 `genres` 필드를 ForeignKey로 해서 배열 형태의 genres 오류 발생
* 하나의 영화에 여러 종류의 장르가 들어가므로 `ManyToManyField`로 !!

## 영화 추천 알고리즘
* 초기 계획한 추천 알고리즘
    * 로그인한 유저가 좋아요 표시한 영화들의 장르 랜덤 추출
    * 장르별 최신 영화 중 좋아요수 상위 추출
    * 이때, 좋아요 누른 영화는 제외

    * 좋아요 누른적 없는 유저라면 최신영화들 중 좋아요 상위 영화 추출

* 실패 후 현재 추천 알고리즘
    * 최신 영화 추출(100개) 중 랜덤 추출(10개)

### 구현 실패한 이유
* 로그인한 유저가 좋아요 누른 영화들의 장르 추출 실패
    * 영화목록은 출력했으나 영화들의 장르 출력을 실패...
    * 실패 원인을 모르겠음(방법 계속 찾아보는 중)


## 추가로 구현하고 싶은 기능
* 영화 정보 - 모달 이용 구현 (새로운 페이지 X)
* 개인 페이지 - 좋아요 누른 영화 목록 확인
* 영화 검색 기능 - 장르, 감독, 영화이름, 출연진 등
* 영화 추천 - 장르별, 나라별, 연령별(영화 관람 등급)


