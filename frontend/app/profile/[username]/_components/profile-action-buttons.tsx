import NewBlogButton from './new-blog-button'

const ProfileActionButtons = () => {
  return (
    <div className="flex flex-col sm:flex-row gap-3 mb-8">
      <NewBlogButton className="gap-2">Write New Blog</NewBlogButton>
    </div>
  )
}

export default ProfileActionButtons
